import json
from datetime import timedelta, timezone
from typing import List

from .api.schemas import ScheduleRequest, ScheduleResponse
from .dynamodb.models import Schedule

JST = timezone(timedelta(hours=9))


def lambda_handler(event, context):
    http_method = event['httpMethod']
    headers = event['headers']
    query_params = event['queryStringParameters'] or {}

    if http_method == 'GET':
        results: List[ScheduleResponse] = get(ScheduleRequest(**query_params))
        return {
            "statusCode": 200,
            "body": json.dumps([result.dict() for result in results])
        }
    else:
        return {"statusCode": 400}


def get(req: ScheduleRequest) -> List[ScheduleResponse]:
    if req.performer_name and req.vol:
        try:
            return [ScheduleResponse.from_orm(Schedule.get(req.performer_name, req.vol))]
        except Schedule.DoesNotExist:
            return []
    elif req.performer_name:
        return [ScheduleResponse.from_orm(schedule) for schedule in Schedule.query(req.performer_name)]
    else:
        return [ScheduleResponse.from_orm(schedule) for schedule in Schedule.scan()]
