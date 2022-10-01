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
        results: List[ProgramReviewResponse] = get(ProgramReviewRequest(**query_params))
        return {
            "statusCode": 200,
            "body": json.dumps([result.dict() for result in results])
        }
    elif http_method == 'POST':
        result: ProgramReviewResponse = post(ProgramReviewRequest(**body))
        return {
            "statusCode": 200,
            "body": json.dumps(result.dict())
        }
    else:
        return {"statusCode": 400}


def get(req: ProgramReviewRequest) -> List[ProgramReviewResponse]:
    ProgramReview.Meta.table_name = f"{ProgramReview.Meta.table_name}_{req.user_id}"

    if not ProgramReview.exists():
        return []
    if req.performer_name and req.vol:
        try:
            return [ProgramReviewResponse.from_orm(ProgramReview.get(req.performer_name, req.vol))]
        except ProgramReview.DoesNotExist:
            return []
    else:
        return [ProgramReviewResponse.from_orm(program_review) for program_review in ProgramReview.scan()]


def post(req: ProgramReviewRequest) -> ProgramReviewResponse:
    ProgramReview.Meta.table_name = f"{ProgramReview.Meta.table_name}_{req.user_id}"

    try:
        Program.get(req.performer_name, req.vol)
    except Program.DoesNotExist:
        return None

    if not ProgramReview.exists():
        ProgramReview.create_table()

    try:
        program_review = ProgramReview.get(req.performer_name, req.vol)
        program_review.star = req.star
    except ProgramReview.DoesNotExist:
        program_review = ProgramReview(req.performer_name, req.vol, star=req.star)

    program_review.save()
    return ProgramReviewResponse.from_orm(program_review)
