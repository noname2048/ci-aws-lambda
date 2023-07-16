from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, fields


class SensorDataDisplay(BaseModel):
    id: int
    sensor_uuid: UUID4
    temperature: float
    humidity: float
    created_at: datetime

    class Config:
        orm_mode = True


class SensorDisplay(BaseModel):
    uuid: UUID4
    name: Optional[str]
    created_at: datetime
    updated_at: datetime
    data: list[SensorDataDisplay]

    class Config:
        orm_mode = True


class SensorCreateForm(BaseModel):
    name: str = fields("", max_length=30)


class SensorDataCreateForm(BaseModel):
    sensor_uuid: UUID4
    temperature: float
    humidity: float
