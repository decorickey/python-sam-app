import json
from datetime import timedelta, timezone
from typing import List

from .api.schemas import ProgramRequest, ScheduleResponse
from .dynamodb.models import Schedule

JST = timezone(timedelta(hours=9))


def lambda_handler(event, context):
    http_method = event['httpMethod']
    headers = event['headers']
    query_params = event['queryStringParameters'] or {}

    if http_method == 'GET':
        res = get(ProgramRequest(**query_params))
        return {
            "statusCode": 200,
            "body": json.dumps(res)
        }
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({})
        }


def get(req: ProgramRequest) -> List[dict]:
    if req.performer and req.vol:
        try:
            schedule_list = [Schedule.get(req.performer, req.vol)]
        except Schedule.DoesNotExist:
            schedule_list = []
    elif req.performer:
        schedule_list = Schedule.query(req.performer)
    else:
        schedule_list = Schedule.scan()

    return [ScheduleResponse.from_orm(schedule).dict() for schedule in schedule_list]
