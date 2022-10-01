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
        results: List[PerformerResponse] = get()
        return {
            "statusCode": 200,
            "body": json.dumps([result.dict() for result in results])
        }
    else:
        return {"statusCode": 400}


def get() -> List[PerformerResponse]:
    try:
        return [PerformerResponse.from_orm(performer) for performer in Performer.scan()]
    except Performer.DoesNotExist:
        return []

