from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from fastapi import Body, Depends, FastAPI, Path, Query, status
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .database import Sensor, SensorData, get_db
from .schemas import (
    SensorCreateForm,
    SensorDataCreateForm,
    SensorDataDisplay,
    SensorDisplay,
)

KST = timezone(offset=timedelta(hours=9))
AT = datetime.utcnow().astimezone(KST)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World", "start_at": AT.strftime("%Y-%m-%d %H:%M:%Sz")}


# @app.get("/sensors")
# async def get_all_sensor(
#     limit: int = Query(..., gt=0, lt=2000),
#     async_session: AsyncSession = Depends(get_db),
#     name: Optional[str] = Query(None),
# ):
#     async with async_session() as session:
#         if name:
#             stmt = select(Sensor).where(Sensor.uuid.contains(name)).limit(limit)
#         else:
#             stmt = select(Sensor).limit(limit)
#         results = session.execute(stmt).scalars().all()

#     return results


# @app.get("/sensor/{sensor_uuid}", response_model=SensorDisplay)
# async def get_one_sensor(
#     sensor_uuid: str = Path(...),
#     async_session: AsyncSession = Depends(get_db),
# ):
#     async with async_session() as session:
#         stmt = select(Sensor).where(Sensor.uuid == sensor_uuid)
#         result = session.execute(stmt).scalars().first()

#     if not result:
#         raise HTTPException(
#             detail="Sensor not found", status_code=status.HTTP_404_NOT_FOUND
#         )

#     return result


# @app.post("/sensor", response_model=SensorDisplay)
# async def create_one_sensor(
#     param: SensorCreateForm = Body(...),
#     async_session: AsyncSession = Depends(get_db),
# ):
#     async with async_session() as session:
#         sensor = Sensor(**param)
#         session.add(sensor)
#         await session.commit()
#         await session.refresh(sensor)

#     return sensor


# @app.get("/data/{sensor_uuid}", response_model=list[SensorDisplay])
# async def get_24hours_data(
#     sensor_uuid: UUID = Path(...),
#     asnyc_session: AsyncSession = Depends(get_db),
# ):
#     lte = datetime.utcnow()
#     gte = lte - timedelta(hours=24)

#     async with asnyc_session() as session:
#         stmt = select(Sensor).where(Sensor.uuid == sensor_uuid).first()
#         result = session.execute(stmt).scalars().first()

#         if not result:
#             raise HTTPException(
#                 detail="Sensor not found", status=status.HTTP_404_NOT_FOUND
#             )

#         stmt = (
#             select(SensorData)
#             .where(SensorData.sensor_uuid == sensor_uuid)
#             .where(SensorData.sensor_uuid >= lte)
#             .where(SensorData.sensor_uuid <= gte)
#             .order_by(SensorData.createdAt.desc())
#         )

#         results = session.execute(stmt).scalars().all()

#     return results


# @app.post("/data/{sensor_uuid}", response_model=SensorDataDisplay)
# async def create_one_data(
#     sensor_uuid: UUID = Path(...),
#     param: SensorDataCreateForm = Body(...),
#     async_session: AsyncSession = Depends(get_db),
# ):
#     async with async_session() as session:
#         stmt = select(Sensor).where(Sensor.uuid == sensor_uuid)
#         result = session.execute(stmt).scalars().first()

#         if not result:
#             raise HTTPException(
#                 detail="Sensor not found", status=status.HTTP_404_NOT_FOUND
#             )

#         data = SensorData(sensor_uuid=sensor_uuid, **param)
#         session.add(data)
#         await session.commit()
#         await session.refresh(data)

#     return data


# handler = Mangum(app, lifespan="off")
