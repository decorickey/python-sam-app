import json
from datetime import timedelta, timezone
from typing import List

from .api.schemas import ProgramGetRequest, ProgramPostRequest, ProgramResponse
from .dynamodb.models import Program

JST = timezone(timedelta(hours=9))


def lambda_handler(event, context):
    http_method = event['httpMethod']
    headers = event['headers']
    query_params = event['queryStringParameters'] or {}
    body = json.loads(event['body']) if event['body'] else {}

    if http_method == 'GET':
        results: List[ProgramResponse] = get(ProgramGetRequest(**query_params))
        return {
            "statusCode": 200,
            "body": json.dumps([result.dict() for result in results])
        }
    elif http_method == 'POST':
        result: ProgramResponse = post(ProgramPostRequest(**body))
        return {
            "statusCode": 200,
            "body": json.dumps(result.dict())
        }
    else:
        return {"statusCode": 400}


def get(req: ProgramGetRequest) -> List[ProgramResponse]:
    if req.performer_name and req.vol:
        try:
            return [ProgramResponse.from_orm(Program.get(req.performer_name, req.vol))]
        except Program.DoesNotExist:
            return []
    elif req.performer_name:
        return [ProgramResponse.from_orm(program) for program in Program.query(req.performer_name)]
    else:
        return [ProgramResponse.from_orm(program) for program in Program.scan()]


def post(req: ProgramPostRequest) -> ProgramResponse:
    try:
        program = Program.get(req.performer_name, req.vol)
        program.old_vol = req.old_vol
    except Program.DoesNotExist:
        program = Program(**req.__dict__)

    program.save()
    return ProgramResponse.from_orm(program)
