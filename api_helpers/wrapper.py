
import requests

from api_helpers.const_and_func import SERVER_ADDRESS


class MainWrapper:

    def __init__(self):
        self.url = f'http://{SERVER_ADDRESS}:3003'
        self.token = None
        self.headers = None
        self.data = None


    def id(self, _id):
        self.url += '{}/'.format(_id)
        return self

    def GET(self):
        resp = requests.get(url=self.url, headers=self.headers)
        return resp

class UsersWrapper(MainWrapper):
    def __init__(self):
        super(UsersWrapper, self).__init__()
        self.url += "users/"

