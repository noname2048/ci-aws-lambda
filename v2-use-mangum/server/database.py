from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel
from sqlalchemy import ForeignKey, func
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from .settings import settings


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Sensor(BaseModel):
    __tablename__ = "sensor"
    uuid: Mapped[str] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(onupdate=func.now())

    data: Mapped[list["SensorData"]] = relationship()


class SensorData(BaseModel):
    __tablename__ = "sensor_data"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sensor_uuid: Mapped[str] = mapped_column(ForeignKey("sensor.uuid"), nullable=False)
    temperature: Mapped[float] = mapped_column(nullable=False)
    humidity: float = mapped_column(nullable=False)
    createdAt: datetime = mapped_column(default=func.now(), nullable=False)


async def get_db() -> AsyncSession:
    engine = create_async_engine(url=settings.DB_URL, echo=settings.DEBUG)
    async_session: AsyncSession = async_sessionmaker(
        engine=engine, expire_on_commit=False
    )
    try:
        yield async_session
    finally:
        await engine.dispose()
