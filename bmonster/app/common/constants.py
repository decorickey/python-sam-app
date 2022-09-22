import urllib.parse
from datetime import timedelta, timezone
from enum import Enum

JST = timezone(timedelta(hours=9))
BASE_URL = "https://www.b-monster.jp"
PAGE_PATH = "reserve/"
URL = urllib.parse.urljoin(BASE_URL, PAGE_PATH)


class StudioCodeList(Enum):
    GINZA = "0001"
    AOYAMA = "0002"
    EBISU = "0003"
    SHINJUKU = "0004"
    IKEBUKURO = "0006"
    SHIBUYA = "0010"
