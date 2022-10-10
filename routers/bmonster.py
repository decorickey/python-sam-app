from typing import List

from fastapi import APIRouter, Header

from bmonster.app import performer, program, program_review, schedule
from bmonster.app.api.schemas import (
    PerformerResponse,
    ProgramGetRequest,
    ProgramPostRequest,
    ProgramResponse,
    ProgramReviewGetRequest,
    ProgramReviewPostRequest,
    ProgramReviewResponse,
    ScheduleRequest,
    ScheduleResponse,
)

router = APIRouter(
    prefix="/bmonster",
    tags=["bmonster"],
)


class Performer:
    @staticmethod
    @router.get("/performer", response_model=List[PerformerResponse])
    def get() -> List[PerformerResponse]:
        return performer.get()


class Program:
    @staticmethod
    @router.get("/program", response_model=List[ProgramResponse])
    def get(performer_name: str = None, vol: str = None) -> List[ProgramResponse]:
        req = ProgramGetRequest(performer_name=performer_name, vol=vol)
        return program.get(req)

    @staticmethod
    @router.post("/program", response_model=ProgramResponse)
    def post(performer_name: str, vol: str, old_vol: str = None) -> ProgramResponse:
        req = ProgramPostRequest(performer_name=performer_name, vol=vol, old_vol=old_vol)
        return program.post(req)


class Schedule:
    @staticmethod
    @router.get("/schedule", response_model=ScheduleResponse)
    def get(performer_name: str, vol: str, old_vol: str = None) -> List[ScheduleResponse]:
        req = ScheduleRequest(performer_name=performer_name, vol=vol, old_vol=old_vol)
        return schedule.get(req)


class ProgramReview:
    @staticmethod
    @router.get("/programReview", response_model=List[ProgramReviewResponse])
    def get(user_id: str = Header(), performer_name: str = None, vol: str = None) -> List[ProgramReviewResponse]:
        req = ProgramReviewGetRequest(
            performer_name=performer_name,
            vol=vol,
        )
        return program_review.get(user_id, req)

    @staticmethod
    @router.post("/programReview", response_model=ProgramReviewResponse)
    def post(user_id: str = Header(), performer_name: str = None, vol: str = None, star: int = None):
        req = ProgramReviewPostRequest(
            performer_name=performer_name,
            vol=vol,
            star=star,
        )
        return program_review.post(user_id, req)
