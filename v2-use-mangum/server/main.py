from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from fastapi import Body, Depends, FastAPI, Path, Query, status
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Base, Sensor, SensorData, engine, get_db
from src.schemas import (
    SensorCreateForm,
    SensorDataCreateForm,
    SensorDataDisplay,
    SensorDisplay,
)
from src.settings import settings

KST = timezone(offset=timedelta(hours=9))
AT = datetime.utcnow().astimezone(KST)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
)


@app.on_event("startup")
async def startup():
    if settings.DEBUG:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {
        "message": "Hello World",
        "start_at": AT.isoformat(timespec="seconds"),
    }


@app.get("/sensors")
async def get_all_sensor(
    limit: int = Query(2000, gt=0, lt=2001),
    async_session: AsyncSession = Depends(get_db),
    name: Optional[str] = Query(None),
):
    async with async_session() as session:
        if name:
            stmt = select(Sensor).where(Sensor.uuid.contains(name)).limit(limit)
        else:
            stmt = select(Sensor).limit(limit)
        results = await session.execute(stmt)
        sensors = results.scalars().all()

    return sensors


@app.get("/sensor/{sensor_uuid}", response_model=SensorDisplay)
async def get_one_sensor(
    sensor_uuid: UUID = Path(..., example="c0d1e9e0-9f9e-4a1a-9b5a-8e8b5d3a0f1a"),
    async_session: AsyncSession = Depends(get_db),
):
    async with async_session() as session:
        stmt = select(Sensor).where(Sensor.uuid == sensor_uuid)
        result = await session.execute(stmt)
        sensor = result.scalars().first()

    if not sensor:
        raise HTTPException(
            detail="Sensor not found", status_code=status.HTTP_404_NOT_FOUND
        )

    return sensor


@app.post("/sensor", response_model=SensorDisplay)
async def create_one_sensor(
    param: SensorCreateForm = Body(...),
    async_session: AsyncSession = Depends(get_db),
):
    async with async_session() as session:
        sensor = Sensor(**param.model_dump())
        session.add(sensor)
        await session.commit()
        await session.refresh(sensor)

    return sensor


@app.get("/data/{sensor_uuid}", response_model=list[SensorDisplay])
async def get_24hours_data(
    sensor_uuid: UUID = Path(...),
    asnyc_session: AsyncSession = Depends(get_db),
):
    lte = datetime.now(tz=KST)
    gte = lte - timedelta(hours=24)

    async with asnyc_session() as session:
        stmt = select(Sensor).where(Sensor.uuid == sensor_uuid)
        result = await session.execute(stmt)
        sensor = result.scalars().first()

        if not sensor:
            raise HTTPException(
                detail="Sensor not found", status=status.HTTP_404_NOT_FOUND
            )

        stmt = (
            select(SensorData)
            .where(SensorData.sensor_uuid == sensor_uuid)
            .where(SensorData.created_at >= lte)
            .where(SensorData.created_at <= gte)
            .order_by(SensorData.created_at.desc())
        )

        results = await session.execute(stmt)
        sensors = results.scalars().all()

    return sensors


@app.post("/data/{sensor_uuid}", response_model=SensorDataDisplay)
async def create_one_data(
    sensor_uuid: UUID = Path(...),
    param: SensorDataCreateForm = Body(...),
    async_session: AsyncSession = Depends(get_db),
):
    async with async_session() as session:
        stmt = select(Sensor).where(Sensor.uuid == sensor_uuid)
        result = await session.execute(stmt)
        sensor = result.scalars().first()

        if not sensor:
            raise HTTPException(
                detail="Sensor not found", status=status.HTTP_404_NOT_FOUND
            )

        data = SensorData(sensor_uuid=sensor_uuid, **param.model_dump())
        session.add(data)
        await session.commit()
        await session.refresh(data)

    return data


handler = Mangum(app, lifespan="off")
