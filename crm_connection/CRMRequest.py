import requests as r


class CRMRequest:
    def __init__(self, url: str, token: str):
        self.__url = url
        self.__token = token

    def get_command(self, command: str) -> r.Response:
        req_url: str = self.__url + command + '/' + self.__token
        return r.get(url=req_url, timeout=5)


from config import config

if __name__ == '__main__':
    req = CRMRequest(url=config.url.get_secret_value(),
                     token=config.crm_token.get_secret_value())

    print(req.get_command('getEmployees'))
