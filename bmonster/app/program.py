import json
from datetime import timedelta, timezone
from typing import List

from .api.schemas import ProgramItem
from .dynamodb.models import Program

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
    if req.performer and req.vol:
        try:
            program_list = [Program.get(req.performer, req.vol)]
        except Program.DoesNotExist:
            return []
    elif req.performer:
        program_list = Program.query(req.performer)
    else:
        program_list = Program.scan()

    return [ProgramItem.from_orm(program).dict() for program in program_list]