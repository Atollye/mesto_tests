
import requests

from api_helpers.const_and_func import BASE_URL


class MainWrapper:

    def __init__(self):
        self.base_url = BASE_URL
        self.url = ''
        self.token = None
        self.headers = None
        self.data = None


    def id(self, _id):
        self.url += '{}/'.format(_id)
        return self

    def GET(self):
        resp = requests.get(url=self.url, headers=self.headers)
        return resp

    def POST(self):
        self.headers = {"Content-Type": "application/json"}
        resp = requests.post(url=self.url, headers=self.headers, json=self.data)
        self.headers = {}
        return resp

    def PATCH(self):
        pass

    def PUT(self):
        pass

    

    def DELETE(self):
        pass


class UsersWrapper(MainWrapper):
    def __init__(self):
        super(UsersWrapper, self).__init__()
        self.url += "users/"

