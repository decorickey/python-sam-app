from typing import Optional

from pydantic import BaseModel


class ScheduleRequest(BaseModel):
    performer_name: Optional[str] = None
    vol: Optional[str] = None
    old_vol: Optional[str] = None


class ScheduleResponse(BaseModel):
    performer_name: str
    vol: str
    schedule_list: Optional[list[dict]] = None

    class Config:
        orm_mode = True


class PerformerResponse(BaseModel):
    name: str

    class Config:
        orm_mode = True


class ProgramGetRequest(BaseModel):
    performer_name: Optional[str] = None
    vol: Optional[str] = None


class ProgramPostRequest(BaseModel):
    performer_name: str
    vol: str
    old_vol: Optional[str] = None


class ProgramResponse(BaseModel):
    performer_name: str
    vol: str
    old_vol: Optional[str] = None

    class Config:
        orm_mode = True


class ProgramReviewGetRequest(BaseModel):
    user_id: str
    performer_name: Optional[str] = None
    vol: Optional[str] = None
    star: Optional[int] = None


class ProgramReviewPostRequest(BaseModel):
    user_id: str
    performer_name: str
    vol: str
    star: Optional[int] = None


class ProgramReviewResponse(BaseModel):
    performer_name: str
    vol: str
    star: Optional[int] = None

    class Config:
        orm_mode = True
