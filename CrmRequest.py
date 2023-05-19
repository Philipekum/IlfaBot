import requests as r
import re
from config import config
import DataModel
from DataModel import Category, Employee, Date, ScheduleData, PostData, VisitItem, EmployeeRequest, Visit, Client
from pydantic import parse_obj_as, ValidationError
from datetime import datetime, timedelta
from exceptions import ElementNotFoundError


class CrmRequest:
    def __init__(self):
        self.__url = config.url.get_secret_value()
        self.__token = config.crm_token.get_secret_value()

        service_url = f'{self.__url}getServices/{self.__token}'
        employee_url = f'{self.__url}getEmployees/{self.__token}'
        self._dates_url = f'{self.__url}getScheduleCache/{self.__token}'
        self._time_url = f'{self.__url}getSchedule/{self.__token}'
        self._post_url = f'{self.__url}createVisit/{self.__token}'

        self._service_data = self._get_parsed_data(service_url, Category)
        self._employee_data = self._get_parsed_data(employee_url, Employee)

    @staticmethod
    def _get_parsed_data(url: str, model: DataModel.Any, params: dict = None) -> DataModel.Any:
        """
        Returns requests parsed with some of DataModel data models.
        Polymorphic behaviour for list of dicts and dicts
        """
        try:
            response = r.get(url=url,
                             params=params)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, list):
                for element in data:
                    model.validate(element)

                return parse_obj_as(list[model], data)

            elif isinstance(data, dict):
                model.validate(data)

                return parse_obj_as(model, data)

        except r.exceptions.RequestException:
            raise ConnectionError(f'Connection to CRM not worked: {url}')

        except ValidationError:
            raise ValueError(f'Data processing Error: {model}')

    def _get_employee_id(self, employee_name: str) -> int:
        """Returns id of employee by name"""
        employee_name = employee_name.casefold().split(" ")

        if len(employee_name) < 3:
            raise ElementNotFoundError(employee_name)

        # Some employees can have full name of 4 words and more
        employee_name = [employee_name.pop(0), employee_name.pop(0), " ".join(employee_name)]

        for employee in self._employee_data:
            if list(map(str.casefold, [employee.lastname, employee.firstname, employee.patronymic])) == employee_name:
                return employee.id

        raise ElementNotFoundError(employee_name)

    def _get_service_id(self, service_name: str) -> int:
        """Returns id of service by name"""
        for category in self._service_data:
            for service in category.services:
                if service.name.casefold() == service_name.casefold():
                    return service.id

        raise ElementNotFoundError(service_name)

    def _check_dates(self, date_to_check: datetime, employee_id: int) -> bool:
        """
        Returns True if date contains employee.
        Due to API restrictions, getSchedule method does not take into account that all times can be busy
        """
        params = {"date": date_to_check.strftime('%Y-%m-%d')}
        all_times: ScheduleData = self._get_parsed_data(self._time_url,
                                                        ScheduleData,
                                                        params=params)

        return employee_id in all_times.employees

    def get_categories(self) -> list[str]:
        """Returns all service categories as a list"""
        picked_categories = []
        for category in self._service_data:
            picked_categories.append(category.name)

        return picked_categories

    def get_services(self, category_name: str = None) -> list[str]:
        """Returns service of a category or all services in default"""
        picked_services = []

        for category in self._service_data:
            if category_name is None or category.name == category_name:
                for service in category.services:
                    picked_services.append(service.name)

        if not picked_services:
            raise ElementNotFoundError(category_name)

        return picked_services

    def get_employees(self, service_name: str = None) -> list[str]:
        """Returns list of employees of service or all employees in default"""
        employees = []
        service_id = None if service_name is None else self._get_service_id(service_name)

        for employee in self._employee_data:
            if service_name is None or service_id in employee.serviceEmployeesIds:
                full_name = ' '.join([employee.lastname, employee.firstname, employee.patronymic]).title()
                employees.append(full_name)

        return employees

    def get_dates(self, employee_name: str) -> list[datetime]:
        """Returns list of free dates of an employee in datetime format"""
        employee_id = self._get_employee_id(employee_name)
        data = self._get_parsed_data(self._dates_url, Date)
        free_dates = []
        for free_date, ids in data.items():
            if employee_id in ids:
                if self._check_dates(free_date, employee_id):
                    free_dates.append(free_date.date())

        return free_dates

    def get_times(self, free_date: datetime, employee_name: str) -> list[datetime]:
        """Returns list of free times of a date and of an employee"""
        free_times = []
        employee_id = self._get_employee_id(employee_name)

        if not isinstance(free_date, datetime):
            raise ElementNotFoundError(free_date)

        params = {"date": free_date.strftime('%Y-%m-%d')}
        schedule_data: ScheduleData = self._get_parsed_data(url=self._time_url,
                                                            model=ScheduleData,
                                                            params=params)

        if employee_id not in schedule_data.employees:
            raise ElementNotFoundError(employee_name)

        for time_intervals in schedule_data.employees.get(employee_id):
            start_time = datetime.combine(free_date, time_intervals.start_time)
            end_time = datetime.combine(free_date, time_intervals.end_time)

            while start_time <= end_time:
                free_times.append(start_time)
                start_time += timedelta(minutes=30)

        return free_times

    @staticmethod
    def format_phone_number(phone_number: str) -> str:
        """Returns telephone number formated to +7(xxx)xxx-xx-xx"""
        cleaned_number = re.sub(r'\D', '', phone_number)

        if cleaned_number.startswith("7") and len(cleaned_number) == 11:
            formatted_number = re.sub(r'^7(\d{3})(\d{3})(\d{2})(\d{2})$', r'+7(\1)\2-\3-\4', cleaned_number)
        elif len(cleaned_number) == 10:
            formatted_number = re.sub(r'^(\d{3})(\d{3})(\d{2})(\d{2})$', r'+7(\1)\2-\3-\4', cleaned_number)
        else:
            raise ElementNotFoundError(phone_number)

        return formatted_number

    def post_data_collector(self, user_name: str, telephone: str, comment: str, picked_employee: str,
                            picked_service: str, picked_date: datetime, picked_time: datetime) -> PostData:
        """Returns verified PostData for post-request"""

        user_name = user_name.title().split(" ")
        firstname, surname, patronymic = [user_name.pop(0), user_name.pop(0), " ".join(user_name)]
        telephone = self.format_phone_number(telephone)
        client_data = Client(firstname=firstname,
                             surname=surname,
                             patronymic=patronymic,
                             telephone=telephone,
                             proccesingOfPersonalData=True)

        employee_id = self._get_employee_id(picked_employee)
        service_id = self._get_service_id(picked_service)
        visit_item_data = VisitItem(employeeId=employee_id,
                                    serviceId=str(service_id),
                                    startTime=datetime.strftime(picked_time, '%H:%M'))

        employee_data = EmployeeRequest(id=employee_id)

        visit_data = Visit(date=datetime.strftime(picked_date, '%Y-%m-%d'),
                           comment=comment)

        data: PostData = PostData(client=client_data,
                                  visitItems=[visit_item_data],
                                  employee=employee_data,
                                  visit=visit_data)

        return data

    def post_data(self, data: PostData):
        """Returns response of a post-request"""
        data = data.dict()
        response = r.post(url=self._post_url, data=data)

        return response
