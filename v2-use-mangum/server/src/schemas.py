from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, Field


class SensorDataDisplay(BaseModel):
    id: int
    sensor_uuid: UUID4
    temperature: float
    humidity: float
    created_at: datetime

    class Config:
        from_attributes = True


class SensorDisplay(BaseModel):
    uuid: UUID4
    name: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SensorCreateForm(BaseModel):
    name: str = Field("", max_length=30)


class SensorDataCreateForm(BaseModel):
    temperature: float = Field(..., exampe=25.0)
    humidity: float = Field(..., example=60.0)
