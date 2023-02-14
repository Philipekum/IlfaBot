import requests as r
from fuzzywuzzy import process
from config import config


class CRMRequest:
    def __init__(self):
        self.__url = config.url.get_secret_value()
        self.__token = config.crm_token.get_secret_value()

        self.service_url = f'{self.__url}getServices/{self.__token}'
        self.service_response = r.get(url=self.service_url)
        self.service_data = self.service_response.json()

        self.employee_url = f'{self.__url}getEmployees/{self.__token}'
        self.employee_response = r.get(url=self.employee_url)

        self.dates_url = f'{self.__url}getScheduleCache/{self.__token}'

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

    def get_categories(self) -> list:
        data = self.service_data
        categories = []
        for service_category in data:
            categories.append(service_category.get("name"))

        return categories

    def get_services(self, category: str = None) -> list:

        # Return all services in default
        if category is None:
            services = []
            for service_category in self.service_response.json():
                for service in service_category["services"]:
                    services.append(service["name"])

            return services

        data = [x for x in self.service_data if x.get("name") == category][0]
        services = []
        self.service_data = data.get("services")

        for service in data.get("services"):
            services.append(service.get("name"))

        return services

    def get_employees(self, service_name: str = None) -> list:
        employee_data: list = self.employee_response.json()
        names = []

        # Return all employees in default
        if service_name is None:
            for emp in employee_data:
                name = emp["lastname"].title() + " " + emp["firstname"].title() + " " + emp["patronymic"].title()
                names.append(name)

            return names

        picked_service_data: dict = [x for x in self.service_data if x.get("name") == service_name][0]
        service_id: int = picked_service_data.get("id")

        for emp in employee_data:
            if service_id in emp["serviceEmployeesIds"]:
                name = emp["lastname"].title() + " " + emp["firstname"].title() + " " + emp["patronymic"].title()
                names.append(name)

        return names

    def get_dates(self, employee: str) -> list:
        data = self.employee_response.json()
        name = employee.split(' ')
        employee_id = None
        for emp in data:
            if emp["lastname"].lower() == name[0].lower() and emp["firstname"].lower() == name[1].lower() and \
                    name[2].lower() == emp["patronymic"].lower():
                employee_id = str(emp["id"])

        date_data = r.get(url=self.dates_url).json()
        dates = []
        for date in date_data:
            if employee_id in date:
                dates.append(date)

        return dates

    def get_times(self, doctor: str, date: str) -> list:
        pass

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
    # print(req.get_categories())
    # print(req.get_services('Хирургия'))
    # print(req.get_employees('Удаление экзостоза'))
    print(req.get_dates('Османова Фарида Ибрагимовна'))
