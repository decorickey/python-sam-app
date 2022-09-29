import json
from datetime import timedelta, timezone
from typing import List

from .api.schemas import ProgramItem, ScheduleResponse
from .dynamodb.models import Schedule

JST = timezone(timedelta(hours=9))


def lambda_handler(event, context):
    http_method = event['httpMethod']
    headers = event['headers']
    query_params = event['queryStringParameters'] or {}

    if http_method == 'GET':
        res = get(ProgramItem(**query_params))
        return {
            "statusCode": 200,
            "body": json.dumps(res)
        }
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({})
        }


def get(req: ProgramItem) -> List[dict]:
    if req.performer_name and req.vol:
        try:
            schedule_list = [Schedule.get(req.performer_name, req.vol)]
        except Schedule.DoesNotExist:
            return []
    elif req.performer_name:
        schedule_list = Schedule.query(req.performer_name)
    else:
        schedule_list = Schedule.scan()

    return [ScheduleResponse.from_orm(schedule).dict() for schedule in schedule_list]
