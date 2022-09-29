import json
from datetime import timedelta, timezone
from typing import List

from .api.schemas import ProgramReviewRequest, ProgramReviewResponse
from .dynamodb.models import Program, ProgramReview

JST = timezone(timedelta(hours=9))


def lambda_handler(event, context):
    http_method = event['httpMethod']
    headers = event['headers']
    query_params = event['queryStringParameters'] or {}
    body = json.loads(event['body']) if event['body'] else {}

    if http_method == 'GET':
        res = get(ProgramReviewRequest(**query_params))
        return {
            "statusCode": 200,
            "body": json.dumps(res)
        }
    elif http_method == 'POST':
        res = post(ProgramReviewRequest(**body))
        return {
            "statusCode": 200,
            "body": json.dumps(res)
        }
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({})
        }


def get(req: ProgramReviewRequest) -> List[dict]:
    ProgramReview.Meta.table_name = f"{ProgramReview.Meta.table_name}_{req.user_id}"

    if not ProgramReview.exists():
        return []
    if req.performer and req.vol:
        try:
            program_review_list = [ProgramReview.get(req.performer, req.vol)]
        except ProgramReview.DoesNotExist:
            return []
    else:
        program_review_list = ProgramReview.scan()

    return [ProgramReviewResponse.from_orm(program_review).dict() for program_review in program_review_list]


def post(req: ProgramReviewRequest) -> dict:
    ProgramReview.Meta.table_name = f"{ProgramReview.Meta.table_name}_{req.user_id}"

    try:
        Program.get(req.performer, req.vol)
    except Program.DoesNotExist:
        return {}

    if not ProgramReview.exists():
        ProgramReview.create_table()

    try:
        program_review = ProgramReview.get(req.performer, req.vol)
        program_review.star = req.star
    except ProgramReview.DoesNotExist:
        program_review = ProgramReview(performer=req.performer, vol=req.vol, star=req.star)

    program_review.save()
    return ProgramReviewResponse.from_orm(program_review).dict()
