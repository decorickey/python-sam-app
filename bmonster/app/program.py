import json
from datetime import timedelta, timezone
from typing import List

from .api.schemas import ProgramRequest, ProgramResponse
from .dynamodb.models import Program

JST = timezone(timedelta(hours=9))


def lambda_handler(event, context):
    http_method = event['httpMethod']
    headers = event['headers']
    query_params = event['queryStringParameters'] or {}
    body = json.loads(event['body']) if event['body'] else {}

    if http_method == 'GET':
        results: List[ProgramResponse] = get(ProgramRequest(**query_params))
        return {
            "statusCode": 200,
            "body": json.dumps([result.dict() for result in results])
        }
    elif http_method == 'POST':
        result: ProgramResponse = post(ProgramRequest(**body))
        return {
            "statusCode": 200,
            "body": json.dumps(result.dict())
        }
    else:
        return {"statusCode": 400}


def get(req: ProgramRequest) -> List[ProgramResponse]:
    if req.performer_name and req.vol:
        try:
            return [ProgramResponse.from_orm(Program.get(req.performer_name, req.vol))]
        except Program.DoesNotExist:
            return []
    elif req.performer_name:
        return [ProgramResponse.from_orm(program) for program in Program.query(req.performer_name)]
    else:
        return [ProgramResponse.from_orm(program) for program in Program.scan()]


def post(req: ProgramRequest) -> ProgramResponse:
    try:
        if req.performer_name and req.vol:
            program = Program.get(req.performer_name, req.vol)
            program.old_vol = req.old_vol
        else:
            return None
    except Program.DoesNotExist:
        program = Program(**req.__dict__)

    program.save()
    return ProgramResponse.from_orm(program)
