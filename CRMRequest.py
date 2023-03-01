import requests as r
# from fuzzywuzzy import process
from config import config
from DataModel import Category, Employee
from pydantic import parse_obj_as
from typing import List, Dict
from datetime import datetime, timedelta


class CRMRequest:
    def __init__(self):
        self.__url = config.url.get_secret_value()
        self.__token = config.crm_token.get_secret_value()

        self.service_url = f'{self.__url}getServices/{self.__token}'
        self.service_response = r.get(url=self.service_url)
        self.service_data = parse_obj_as(List[Category], self.service_response.json())

        self.employee_url = f'{self.__url}getEmployees/{self.__token}'
        self.employee_response = r.get(url=self.employee_url)
        self.employee_data = parse_obj_as(List[Employee], self.employee_response.json())

        self.dates_url = f'{self.__url}getScheduleCache/{self.__token}'

        self.time_url = f'{self.__url}getSchedule/{self.__token}'

        self.post_data = {
            "client": {
                "firstname": "Иван",
                "surname": "Иванов",
                "patronymic": "",
                "telephone": "+7(904)243-23-43",
                "proccesingOfPersonalData": True
            },
            "visitItems": [
                {
                    "employeeId": "2",
                    "serviceId": 163,
                    "startTime": "14:00"
                }
            ],
            "employee": {
                "id": 0
            },
            "visit": {
                "date": "2022-01-28",
                "comment": "Позвоните мне"
            }
        }

    def __get_employee_id(self, employee_name: str) -> str:
        """Gets id of employee as str"""
        employee_name = employee_name.upper().split(" ")
        employee_name = [employee_name.pop(0), employee_name.pop(0), " ".join(employee_name)]
        for employee in self.employee_data:
            if list(map(str.upper, [employee.lastname, employee.firstname, employee.patronymic])) == employee_name:
                return str(employee.id)

    def __get_service_id(self, service_name: str) -> int:
        """Gets id of service"""
        for category in self.service_data:
            for service in category.services:
                if service.name == service_name:
                    return service.id

    def get_categories(self) -> List[str]:
        """Returns all service categories as a list"""
        picked_categories = []
        for category in self.service_data:
            picked_categories.append(category.name)

        return picked_categories

    def get_services(self, category_name: str = None) -> List[str]:
        """Returns service of a category or all services in default"""
        picked_services = []

        if category_name is None:
            for category in self.service_data:
                for service in category.services:
                    picked_services.append(service.name)

            return picked_services

        for category in self.service_data:
            if category.name == category_name:
                for service in category.services:
                    picked_services.append(service.name)

                return picked_services

    def get_employees(self, service_name: str = None) -> List[str]:
        """Return list of employees of service or all employees in default"""
        employees = []
        if service_name is None:
            for employee in self.employee_data:
                full_name = ' '.join([employee.lastname, employee.firstname, employee.patronymic]).title()
                employees.append(full_name)

            return employees

        service_id = self.__get_service_id(service_name)
        for employee in self.employee_data:
            if service_id in employee.serviceEmployeesIds:
                full_name = ' '.join([employee.lastname, employee.firstname, employee.patronymic]).title()
                employees.append(full_name)

                return employees

    def get_dates(self, employee_name: str) -> List[datetime.date]:
        """Returns list of free dates of an employee"""
        employee_id = self.__get_employee_id(employee_name)

        date_data: Dict[str, Dict[str, bool]] = r.get(url=self.dates_url).json()

        free_dates = []

        for free_date, ids in date_data.items():
            if employee_id in ids:
                free_date = datetime.strptime(free_date, '%Y-%m-%d').date()
                free_dates.append(free_date)

        return free_dates

    def get_times(self, date_obj: datetime.date, employee_name: str) -> List[datetime]:
        """Returns list of free times of a date and of an employee"""
        free_times = []
        employee_id = self.__get_employee_id(employee_name)
        time_intervals = r.get(url=self.time_url,
                               params={"date": date_obj.strftime('%Y-%m-%d')}).json()["employees"][employee_id]

        for interval in time_intervals:
            start_time = datetime.combine(date_obj,
                                          datetime.strptime(interval['startTime'], '%H:%M').time())

            end_time = datetime.combine(date_obj,
                                        datetime.strptime(interval['endTime'], '%H:%M').time())

            while start_time <= end_time:
                free_times.append(start_time)
                start_time += timedelta(minutes=30)

        return free_times

    # def search(self, request: str) -> list:
    #     coincidences = process.extract(request, self.services.keys())
    #     res = []
    #
    #     for i in coincidences:
    #         if i[1] >= 75:
    #             res.append(i[0])
    #
    #     return res


if __name__ == '__main__':
    req = CRMRequest()
    dates = req.get_dates('Гадирова Айнур Захир Кызы')
    print(req.get_times(dates[0], 'Гадирова Айнур Захир Кызы'))

