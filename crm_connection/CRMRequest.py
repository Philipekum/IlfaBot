import requests as r


class CRMRequest:
    def __init__(self, url: str, token: str):
        self.__url = url
        self.__token = token

    def get_command(self, command: str) -> list:
        req_url: str = self.__url + command + '/' + self.__token
        return r.get(req_url).json()
