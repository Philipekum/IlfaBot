import pydantic
import requests as r

import DataModel
from config import config
from DataModel import Category, Employee
from pydantic import parse_obj_as
from datetime import datetime, timedelta


class CRMRequest:
    def __init__(self):
        self.__url = config.url.get_secret_value()
        self.__token = config.crm_token.get_secret_value()

        service_url = f'{self.__url}getServices/{self.__token}'
        employee_url = f'{self.__url}getEmployees/{self.__token}'
        self.dates_url = f'{self.__url}getScheduleCache/{self.__token}'
        self.time_url = f'{self.__url}getSchedule/{self.__token}'

        try:
            self.service_data = self._get_parsed_data(service_url, Category)

        except (ConnectionError, ValueError) as e:
            print(e)

        try:
            self.employee_data = self._get_parsed_data(employee_url, Employee)

        except (ConnectionError, ValueError) as e:
            print(e)

        # self.post_data = {
        #     "client": {
        #         "firstname": "Иван",
        #         "surname": "Иванов",
        #         "patronymic": "",
        #         "telephone": "+7(904)243-23-43",
        #         "proccesingOfPersonalData": True
        #     },
        #     "visitItems": [
        #         {
        #             "employeeId": "2",
        #             "serviceId": 163,
        #             "startTime": "14:00"
        #         }
        #     ],
        #     "employee": {
        #         "id": 0
        #     },
        #     "visit": {
        #         "date": "2022-01-28",
        #         "comment": "Позвоните мне"
        #     }
        # }

    @staticmethod
    def _get_parsed_data(url: str, model: DataModel.Any) -> list:
        try:
            response = r.get(url)
            response.raise_for_status()
            data = response.json()

            for element in data:
                model.validate(element)

            return parse_obj_as(list[model], data)

        except r.exceptions.RequestException:
            raise ConnectionError(f'Ошибка при получении данных: {url}')

        except pydantic.ValidationError:
            raise ValueError(f'Ошибка при обработке данных: {url}')

    def _get_employee_id(self, employee_name: str) -> str:
        """Gets id of employee as str"""
        employee_name = employee_name.casefold().split(" ")
        employee_name = [employee_name.pop(0), employee_name.pop(0), " ".join(employee_name)]
        for employee in self.employee_data:
            if list(map(str.casefold, [employee.lastname, employee.firstname, employee.patronymic])) == employee_name:
                return str(employee.id)

        raise ValueError(f'Employee {employee_name} not found')

    def _get_service_id(self, service_name: str) -> int:
        """Gets id of service"""
        for category in self.service_data:
            for service in category.services:
                if service.name.casefold() == service_name.casefold():
                    return service.id

        raise ValueError(f'Service {service_name} not found')

    def get_categories(self) -> list[str]:
        """Returns all service categories as a list"""
        picked_categories = []
        for category in self.service_data:
            picked_categories.append(category.name)

        return picked_categories

    def get_services(self, category_name: str = None) -> list[str]:
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

    def get_employees(self, service_name: str = None) -> list[str]:
        """Return list of employees of service or all employees in default"""
        employees = []
        if service_name is None:
            for employee in self.employee_data:
                full_name = ' '.join([employee.lastname, employee.firstname, employee.patronymic]).title()
                employees.append(full_name)

            return employees

        service_id = self._get_service_id(service_name)
        for employee in self.employee_data:
            if service_id in employee.serviceEmployeesIds:
                full_name = ' '.join([employee.lastname, employee.firstname, employee.patronymic]).title()
                employees.append(full_name)

                return employees

    def get_dates(self, employee_name: str) -> list[str]:
        """Returns list of free dates of an employee"""
        employee_id = self._get_employee_id(employee_name)

        date_data: dict[str, dict[str, bool]] = r.get(url=self.dates_url).json()

        free_dates = []
        week = {0: 'ПН', 1: 'ВТ', 2: 'СР', 3: 'ЧТ', 4: 'ПТ', 5: 'СБ', 6: 'ВС'}

        for free_date, ids in date_data.items():
            if employee_id in ids:
                free_date = datetime.strptime(free_date, '%Y-%m-%d')
                formated_date = week[free_date.weekday()] + free_date.strftime(' %d.%m')
                free_dates.append(formated_date)

        return free_dates

    def get_times(self, date_obj: datetime, employee_name: str) -> list[str] | None:
        """Returns list of free times of a date and of an employee"""
        free_times = []
        time_intervals = []
        employee_id = self._get_employee_id(employee_name)
        params = {"date": date_obj.strftime('%Y-%m-%d')}
        all_time_intervals = r.get(url=self.time_url,
                                   params=params).json()

        if all_time_intervals["employees"]:
            if employee_id in all_time_intervals["employees"]:
                time_intervals = all_time_intervals["employees"][employee_id]
        else:
            return None

        for interval in time_intervals:
            start_time = datetime.combine(date_obj,
                                          datetime.strptime(interval['startTime'], '%H:%M').time())

            end_time = datetime.combine(date_obj,
                                        datetime.strptime(interval['endTime'], '%H:%M').time())

            while start_time <= end_time:
                free_times.append(start_time.strftime('%H:%M'))
                start_time += timedelta(minutes=30)

        return free_times


if __name__ == '__main__':
    req = CRMRequest()
    print(req.service_data)
