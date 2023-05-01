from pydantic import BaseModel
from typing import Any, List


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
    services: List[Service]
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
