from pydantic import BaseModel, Field
from datetime import datetime, time
from typing import Any


class Service(BaseModel):
    name: str
    categoryID: int
    id: int
    price: float
    duration: float
    discountSum: int
    visible: bool
    photoID: Any
    ozOrder: int
    ozDescription: Any
    ozDescriptionPhoto: Any
    priceFrom: Any
    priceTill: Any
    isRangePrice: bool
    priceTillDiscountSum: int
    primaryKey: int
    modelClass: str
    uniqueKey: str


class Category(BaseModel):
    id: int
    name: str
    parentID: Any
    haveServices: bool
    services: list[Service]
    children: list
    ozOrder: int


class Employee(BaseModel):
    id: int
    lastname: str
    firstname: str
    patronymic: str
    positionName: str
    extraCharge: float
    serviceEmployeesIds: list


class Date(BaseModel):
    date_values: dict[str, dict[str, bool]]

    @classmethod
    def validate(cls, value):
        validated_values = {}

        for date_str, inner_dict in value.items():
            date = datetime.strptime(date_str, '%Y-%m-%d')
            inner_list = list(map(int, inner_dict.keys()))
            validated_values[date] = inner_list

        return validated_values


class Schedule(BaseModel):
    start_time: time = Field(..., alias='startTime', strptime=True)
    end_time: time = Field(..., alias='endTime', strptime=True)


class ScheduleData(BaseModel):
    employees: dict[int, list[Schedule]]
    org_work_time: Schedule = Field(..., alias='orgWorkTime', strptime=True)
