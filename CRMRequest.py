import requests as r
from config import config


class CRMRequest:
    def __init__(self):
        self.__url = config.url.get_secret_value()
        self.__token = config.crm_token.get_secret_value()

        get_service_url: str = f'{self.__url}getServices/{self.__token}'
        get_employee_url: str = f'{self.__url}getEmployee/{self.__token}'

        # Makes a dict with keys as ['name'] of dictionary in a list and dictionaries as values
        name_dictator = lambda response: dict(
            zip(
                [element['name'] for element in response],
                response
            )
        )

        service_response = r.get(url=get_service_url, timeout=5).json()

        self.services = name_dictator(service_response)

        # employee_response = r.get(url=get_employee_url, timeout=5).json()
        #
        # self.employees = name_dictator(employee_response)

    # def get_service_names(self, category: str) -> list:
    #     if category not in self.services:
    #         raise ValueError
    #
    #     for i in self.services:
    #         if i['name'] == category:
    #
    #             for j in i['services']:
    #                 res.append(j['name'])
    #
    #             break
    #
    #     return res

    # def get_employee_by_service(self, service: str) -> list:
    #     res = []
    #     if service not in self.services[]


from config import config

if __name__ == '__main__':
    req = CRMRequest()
    # services = req.get_command('getServices').json()
    print(req.services.keys())
