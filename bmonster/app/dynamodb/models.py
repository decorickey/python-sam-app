import os
from datetime import datetime, timedelta

from pynamodb.attributes import ListAttribute, NumberAttribute, TTLAttribute, UnicodeAttribute
from pynamodb.models import Model

from ..common.constants import JST


def dynamodb_migrate():
    if not Performer.exists():
        Performer.create_table()

    if not Program.exists():
        Program.create_table()

    # スケジュールは毎回最新化する
    if Schedule.exists():
        Schedule.delete_table()
    Schedule.create_table()


class BaseMeta:
    region = os.getenv('REGION')
    host = os.getenv('DYNAMODB_HOST') or None
    billing_mode = os.getenv('BILLING_MODE')


class Performer(Model):
    class Meta(BaseMeta):
        table_name = 'performer'

    name = UnicodeAttribute(hash_key=True)
    ttl = TTLAttribute(default=datetime.now(JST) + timedelta(days=365))

    def __str__(self):
        return self.name


class Program(Model):
    class Meta(BaseMeta):
        table_name = 'program'

    performer_name = UnicodeAttribute(hash_key=True)
    vol = UnicodeAttribute(range_key=True)
    old_vol = UnicodeAttribute(null=True)
    ttl = TTLAttribute(default=datetime.now(JST) + timedelta(days=365))


class Schedule(Model):
    class Meta(BaseMeta):
        table_name = 'schedule'

    performer_name = UnicodeAttribute(hash_key=True)
    vol = UnicodeAttribute(range_key=True)
    schedule_list = ListAttribute(null=True)
    ttl = TTLAttribute(default=datetime.now(JST) + timedelta(days=7))


class ProgramReview(Model):
    @classmethod
    def generate_table_name(cls, user_id: str):
        cls.Meta.table_name = f"program_review_{user_id}"

    class Meta(BaseMeta):
        table_name = 'program_review'

    performer_name = UnicodeAttribute(hash_key=True)
    vol = UnicodeAttribute(range_key=True)
    star = NumberAttribute()
