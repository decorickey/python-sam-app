from typing import List, Optional

from pydantic import BaseModel, Field


class ScheduleResponse(BaseModel):
    performer: str
    vol: str
    scheduleList: List[dict] = Field(..., alias="schedule_list")

    class Config:
        orm_mode = True


class ProgramItem(BaseModel):
    performer: Optional[str] = None
    vol: Optional[str] = None
    old_vol: Optional[str] = None

    class Config:
        orm_mode = True


class ProgramReviewRequest(BaseModel):
    user_id: str
    performer: Optional[str] = None
    vol: Optional[str] = None
    star: Optional[int] = None


class ProgramReviewResponse(BaseModel):
    performer: Optional[str] = None
    vol: Optional[str] = None
    star: Optional[int] = None

    class Config:
        orm_mode = True
