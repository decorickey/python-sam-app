import json
from datetime import timedelta, timezone
from typing import List

from .api.schemas import PerformerResponse
from .dynamodb.models import Performer

JST = timezone(timedelta(hours=9))


def lambda_handler(event, context):
    http_method = event['httpMethod']
    headers = event['headers']
    query_params = event['queryStringParameters'] or {}
    body = json.loads(event['body']) if event['body'] else {}

    if http_method == 'GET':
        res = get()
        return {
            "statusCode": 200,
            "body": json.dumps(res)
        }
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({})
        }


def get() -> List[dict]:
    try:
        performer_list = Performer.scan()
        return [PerformerResponse.from_orm(performer).dict() for performer in performer_list]
    except Performer.DoesNotExist:
        return []

