from typing import List, Optional

from pydantic import BaseModel, Field


class ScheduleResponse(BaseModel):
    performer_name: str
    vol: str
    scheduleList: Optional[list[dict]] = Field(..., alias="schedule_list")

    class Config:
        orm_mode = True


class PerformerResponse(BaseModel):
    name: str

    class Config:
        orm_mode = True


class ProgramItem(BaseModel):
    performer_name: Optional[str] = None
    vol: Optional[str] = None
    old_vol: Optional[str] = None

    class Config:
        orm_mode = True


class ProgramReviewRequest(BaseModel):
    user_id: str
    performer_name: Optional[str] = None
    vol: Optional[str] = None
    star: Optional[int] = None


class ProgramReviewResponse(BaseModel):
    performer_name: Optional[str] = None
    vol: Optional[str] = None
    star: Optional[int] = None

    class Config:
        orm_mode = True
