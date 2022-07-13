# coding: utf8
# ===================================
# Author: yumingmin
# File: main.py
# Cate: FastAPI
# Create time: 2022/7/8 10:32
# Update time: 
# ===================================

import requests
from typing import List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request, status
from fastapi.templating import Jinja2Templates
from pydantic import HttpUrl
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import engine, Base, SessionLocal
from .models import City, Data

application = APIRouter()
template = Jinja2Templates(directory="./templates")
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@application.post("/create_city", response_model=schemas.ReadCity)
async def create_city(city: schemas.CreateCity, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db, name=city.province)

    if db_city:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="City already registered!"
        )

    return crud.create_city(db=db, city=city)


@application.get("/get_city/{city}", response_model=schemas.ReadCity)
async def get_city(city: str, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db, name=city)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@application.get("/get_cities", response_model=List[schemas.ReadCity])
async def get_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cities = crud.get_cities(db, skip=skip, limit=limit)
    return cities


@application.post("/create_data", response_model=schemas.ReadData)
async def create_data_for_city(city: str, data: schemas.CreateData, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db, name=city)
    data = crud.create_city_data(db, data, city_id=db_city.id)
    return data


@application.get("/get_data")
def get_data(city: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    data = crud.get_data(db, city, skip, limit)
    return data


def bg_task(url: HttpUrl, db: Session):
    """这里注意一个坑，不要在后台任务的参数中 db: Session = Depends(get_db) 这样导入依赖"""
    city_data = requests.get(url=f"{url}?source=jhu&country_code=CN&timelines=false")

    if 200 == city_data.status_code:
        db.query(City).delete()  # 同步数据前先清空原有数据

        for location in city_data.json()["locations"]:
            city = {
                "province": location["province"],
                "country": location["country"],
                "country_code": "CN",
                "country_population": location["country_population"]
            }
            crud.create_city(db, city=schemas.CreateCity(**city))

    coronavirus_data = requests.get(url=f"{url}?source=jhu&country_code=CN&timelines=true")

    if 200 == coronavirus_data.status_code:
        db.query(Data).delete()

        for city in coronavirus_data.json()["locations"]:
            db_city = crud.get_city_by_name(db, name=city["province"])

            for date, confirmed in city["timelines"]["confirmed"]["timeline"].items():
                data = {
                    "date": date.split("T")[0],
                    "confirmed": confirmed,
                    "deaths": city["timelines"]["deaths"]["timeline"][date],
                    "recovered": 0
                }
                crud.create_city_data(db, data=schemas.CreateData(**data), city_id=db_city.id)


@application.get("/sync_coronavirus_data/jhu")
async def sync_coronavirus_data(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """从 Johns Hopkins University 同步 COVID-19 数据"""
    background_tasks.add_task(bg_task, "https://coronavirus-tracker-api.herokuapp.com/v2/locations", db)
    return {"message": "正在后台同步数据..."}


@application.get("/")
async def coronavirus(
    request: Request,
    city: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    data = crud.get_data(db, city, skip, limit)
    return template.TemplateResponse("home.html", {
        "request": request,
        "data": data,
        "sync_data_url": "/coronavirus/sync_coronavirus_data/jhu"
    })
