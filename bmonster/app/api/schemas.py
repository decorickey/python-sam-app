from typing import List, Optional

from pydantic import BaseModel, Field


class ScheduleResponse(BaseModel):
    performer: str
    vol: str
    scheduleList: List[dict] = Field(..., alias="schedule_list")

    class Config:
        orm_mode = True


class ProgramRequest(BaseModel):
    performer: Optional[str] = None
    vol: Optional[str] = None
