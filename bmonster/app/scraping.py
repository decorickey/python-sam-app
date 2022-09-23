import json
from collections import namedtuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List

import requests
from bs4 import BeautifulSoup

from .api.schemas import ScheduleResponse
from .common.constants import JST, URL, StudioCodeList
from .dynamodb.models import Performer, Program, Schedule, dynamodb_migrate


def lambda_handler(event, context):
    dynamodb_migrate()
    res = main()
    return {
        "statusCode": 200,
        "body": json.dumps(res)
    }


@dataclass
class ScrapingItem:
    performer: str
    vol: str
    studio: str
    start_datetime: datetime


def main() -> List[dict]:
    # スクレイピング実行して最新のレスケ一覧取得
    item_list: List[ScrapingItem] = []
    for studio in StudioCodeList.__members__.values():
        item_list += scraping(studio_name=studio.name, studio_code=studio.value)

    # パフォーマー一覧を取得（setで重複を排除）
    performer_name_set: set = {item.performer for item in item_list}
    performer_list: List[Performer] = [Performer(performer_name) for performer_name in performer_name_set]
    with Performer.batch_write() as batch:
        for performer in performer_list:
            batch.save(performer)

    # プログラム一覧を取得（setで重複を排除）
    ProgramKey = namedtuple('ProgramKey', 'performer vol')
    program_set: set = {ProgramKey(item.performer, item.vol) for item in item_list}
    program_list: List[Program] = [Program(program_key.performer, program_key.vol) for program_key in program_set]
    with Program.batch_write() as batch:
        for program in program_list:
            batch.save(program)

    # スケジュール一覧を取得
    schedule_dict = {}
    for item in item_list:
        schedule_key = ProgramKey(item.performer, item.vol)
        schedule_value = {"studio": item.studio, "startDatetime": item.start_datetime.isoformat()}
        if not schedule_dict.get(schedule_key):
            schedule_dict[schedule_key] = [schedule_value]
        else:
            schedule_dict[schedule_key].append(schedule_value)
    schedule_list: List[Schedule] = [
        Schedule(performer=key.performer, vol=key.vol, schedule_list=value) for key, value in schedule_dict.items()
    ]
    with Schedule.batch_write() as batch:
        for schedule in schedule_list:
            batch.save(schedule)

    return [ScheduleResponse.from_orm(schedule).dict() for schedule in schedule_list]


def scraping(studio_name: str,
             studio_code: str,
             now: datetime = None) -> List[ScrapingItem]:
    if now is None:
        now = datetime.now(JST)
    item_list: List[ScrapingItem] = []

    # HTML取得
    r = requests.get(URL, params={"studio_code": studio_code})
    try:
        r.raise_for_status()
    except Exception as e:
        raise e

    # HTML解析
    soup = BeautifulSoup(r.text, features="html.parser")
    week = soup.select("body div#scroll-box div.grid div.flex-no-wrap")
    date = now
    for day in week:
        panels = day.select("li.panel")
        for panel in panels:
            time = panel.select("p.tt-time")
            performer = panel.select("p.tt-instructor")
            program = panel.select("p.tt-mode")

            if time and performer and program:
                # プログラム開始時間（HH:MM）
                hour = int(time[0].text[:2])
                minute = int(time[0].text[3:5])
                # パフォーマー
                performer = performer[0].text
                # プログラム名（リミテッド表記を削除）
                program = program[0]["data-program"]
                program = program if "(l)" not in program else program[:-3]
                # パフォーマー名またはプログラム名が未定の場合はスキップ
                if not performer or not program:
                    continue

                item_list.append(ScrapingItem(
                    performer,
                    program,
                    studio_name,
                    datetime(year=date.year, month=date.month, day=date.day, hour=hour, minute=minute, tzinfo=JST)
                ))

        date += timedelta(days=1)

    return item_list
