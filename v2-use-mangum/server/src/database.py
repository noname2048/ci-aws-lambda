from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.settings import settings


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Sensor(Base):
    __tablename__ = "sensor"
    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(default="")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
    data: Mapped[list["SensorData"]] = relationship(
        "SensorData",
        back_populates="sensor",
        lazy="joined",
    )


class SensorData(Base):
    __tablename__ = "sensor_data"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sensor_uuid: Mapped[str] = mapped_column(ForeignKey("sensor.uuid"), nullable=False)
    temperature: Mapped[float] = mapped_column(nullable=False)
    humidity: Mapped[float] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )
    sensor: Mapped[Sensor] = relationship("Sensor", back_populates="data")


engine = create_async_engine(url=settings.DB_URL, echo=settings.DEBUG)


async def get_db() -> AsyncSession:
    async_session: AsyncSession = async_sessionmaker(
        bind=engine, expire_on_commit=False
    )
    try:
        yield async_session
    finally:
        await engine.dispose()
