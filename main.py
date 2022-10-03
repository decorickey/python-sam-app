from typing import List

from fastapi import FastAPI

from bmonster.app import performer, program, program_review, schedule
from bmonster.app.api.schemas import (
    PerformerResponse,
    ProgramGetRequest,
    ProgramPostRequest,
    ProgramResponse,
)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


class Performer:
    @staticmethod
    @app.get("/performer", response_model=List[PerformerResponse])
    def get() -> List[PerformerResponse]:
        return performer.get()


class Program:
    @staticmethod
    @app.get("/program", response_model=List[ProgramResponse])
    def get(performer_name: str = None, vol: str = None) -> List[ProgramResponse]:
        req = ProgramGetRequest(performer_name=performer_name, vol=vol)
        return program.get(req)

    @staticmethod
    @app.post("/program", response_model=ProgramResponse)
    def post(performer_name: str, vol: str, old_vol: str = None) -> ProgramResponse:
        req = ProgramPostRequest(performer_name=performer_name, vol=vol, old_vol=old_vol)
        return program.post(req)
