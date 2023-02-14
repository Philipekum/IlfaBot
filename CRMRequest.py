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

    def get_categories(self) -> list:
        data = self.service_data
        categories = []
        for service_dict in data:
            categories.append(service_dict.get('name'))

        return categories

    def get_services(self, category: str = None) -> list:
        if category is None:
            # return all services in each category
            pass

        data = [x for x in self.service_data if x.get('name') == category][0]
        self.service_data = data.get('services')
        services = []

        for service in data.get('services'):
            services.append(service.get('name'))

        return services

    def get_employees(self, service_name: str = None) -> dict:
        if service_name is None:
            # return all employees
            pass

        employee_data: list = self.employee_response.json()
        picked_service_data: dict = [x for x in self.service_data if x.get('name') == service_name][0]
        service_id: int = picked_service_data.get('id')
        names = []
        ids = []

        for emp in employee_data:
            if service_id in emp['serviceEmployeesIds']:
                name = emp['lastname'].title() + ' ' + emp['firstname'].title() + ' ' + emp['patronymic'].title()
                names.append(name)
                ids.append(emp['id'])

        res = dict(zip(ids, names))

        return res

    def get_dates(self, doctor: str) -> list:
        pass

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
    print(req.get_categories())
    print(req.get_services('Хирургия'))
    print(req.get_employees('Удаление экзостоза'))
