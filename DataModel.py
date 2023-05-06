from pydantic import BaseModel, parse_obj_as
from datetime import datetime
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


if __name__ == '__main__':
    data = {'2023-05-06': {'1': True, '2': True, '29': True, '31': True},
            '2023-05-07': {'1': True, '2': True, '8': True, '29': True},
            '2023-05-08': {'8': True, '31': True, '35': True}, '2023-05-09': {'31': True, '35': True},
            '2023-05-10': {'1': True, '8': True, '29': True},
            '2023-05-11': {'1': True, '2': True, '31': True, '35': True},
            '2023-05-12': {'8': True, '29': True, '31': True},
            '2023-05-13': {'1': True, '2': True, '29': True, '31': True},
            '2023-05-14': {'1': True, '2': True, '8': True, '29': True}, '2023-05-15': {'31': True, '35': True},
            '2023-05-16': {'2': True, '31': True, '35': True}, '2023-05-17': {'1': True, '29': True},
            '2023-05-18': {'1': True, '2': True, '31': True, '35': True}, '2023-05-19': {'29': True, '31': True},
            '2023-05-20': {'29': True, '31': True}, '2023-05-21': {'29': True, '35': True},
            '2023-05-22': {'8': True, '31': True, '35': True}, '2023-05-23': {'2': True, '31': True, '35': True},
            '2023-05-24': {'1': True, '8': True, '29': True},
            '2023-05-25': {'1': True, '2': True, '31': True, '35': True},
            '2023-05-26': {'8': True, '29': True, '31': True},
            '2023-05-27': {'1': True, '2': True, '29': True, '31': True},
            '2023-05-28': {'1': True, '2': True, '8': True, '29': True},
            '2023-05-29': {'8': True, '31': True, '35': True}, '2023-05-30': {'31': True, '35': True},
            '2023-05-31': {'1': True, '8': True, '29': True},
            '2023-06-01': {'1': True, '2': True, '31': True, '35': True},
            '2023-06-02': {'8': True, '29': True, '31': True},
            '2023-06-03': {'1': True, '2': True, '29': True, '31': True},
            '2023-06-04': {'1': True, '2': True, '8': True, '29': True}, '2023-06-05': {'8': True, '31': True},
            '2023-06-06': {'2': True, '31': True}, '2023-06-07': {'1': True, '8': True, '29': True},
            '2023-06-08': {'1': True, '2': True, '31': True}, '2023-06-09': {'8': True, '29': True, '31': True},
            '2023-06-10': {'1': True, '2': True, '31': True},
            '2023-06-11': {'1': True, '2': True, '8': True, '29': True},
            '2023-06-12': {'8': True, '31': True, '35': True}, '2023-06-13': {'2': True, '31': True, '35': True},
            '2023-06-14': {'1': True, '8': True, '29': True}, '2023-06-15': {'2': True, '31': True, '35': True},
            '2023-06-16': {'8': True, '31': True}, '2023-06-17': {'2': True, '31': True},
            '2023-06-18': {'2': True, '8': True, '29': True}, '2023-06-19': {'8': True, '31': True, '35': True},
            '2023-06-20': {'2': True, '31': True, '35': True}, '2023-06-21': {'1': True, '29': True},
            '2023-06-22': {'1': True, '2': True, '31': True, '35': True}, '2023-06-23': {'8': True, '31': True},
            '2023-06-24': {'1': True, '2': True, '31': True},
            '2023-06-25': {'1': True, '2': True, '8': True, '29': True},
            '2023-06-26': {'8': True, '31': True, '35': True}, '2023-06-27': {'2': True, '31': True, '35': True},
            '2023-06-28': {'1': True, '8': True, '29': True},
            '2023-06-29': {'1': True, '2': True, '31': True, '35': True},
            '2023-06-30': {'8': True, '29': True, '31': True},
            '2023-07-01': {'1': True, '2': True, '29': True, '31': True}, '2023-07-02': {'2': True},
            '2023-07-05': {'1': True, '8': True, '29': True},
            '2023-07-08': {'1': True, '2': True, '29': True, '31': True}, '2023-07-09': {'2': True},
            '2023-07-15': {'1': True, '2': True, '29': True, '31': True},
            '2023-07-22': {'1': True, '2': True, '29': True, '31': True},
            '2023-07-29': {'1': True, '2': True, '29': True, '31': True}}
    parsed_data = parse_obj_as(Date, data)
    print(parsed_data)
