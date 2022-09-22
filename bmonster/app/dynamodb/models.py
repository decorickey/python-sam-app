import os
from datetime import datetime, timedelta

from pynamodb.attributes import ListAttribute, TTLAttribute, UnicodeAttribute
from pynamodb.models import Model

from ..common.constants import JST


def dynamodb_migrate():
    if not Performer.exists():
        Performer.create_table()

    if not Program.exists():
        Program.create_table()

    if not Schedule.exists():
        Schedule.create_table()

    # if not ProgramReviewIndex.exists():
    #     ProgramReviewIndex.create_table()


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

    performer = UnicodeAttribute(hash_key=True)
    vol = UnicodeAttribute(range_key=True)
    ttl = TTLAttribute(default=datetime.now(JST) + timedelta(days=365))


class Schedule(Model):
    class Meta(BaseMeta):
        table_name = 'schedule'

    performer = UnicodeAttribute(hash_key=True)
    vol = UnicodeAttribute(range_key=True)
    schedule_list = ListAttribute()
    ttl = TTLAttribute(default=datetime.now(JST) + timedelta(days=7))


# class ProgramReview(Model):
#     class Meta(BaseMeta):
#         table_name = 'program_review'
#
#     performer = UnicodeAttribute(hash_key=True)
#     vol = UnicodeAttribute(range_key=True)
#     star = NumberAttribute()