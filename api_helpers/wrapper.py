
import requests

class MainWrapper:

    def __init__(self):
        self.base_url = ''
        self.url = ''
        self.token = None
        self.headers = {}
        self.data = None


    def id(self, _id):
        self.url += '{}/'.format(_id)
        return self

    def GET(self):
        resp = requests.get(url=self.url, headers=self.headers)
        return resp

    def POST(self):
        hdrs = self.headers.copy()
        hdrs.update({"Content-Type": "application/json"})
        resp = requests.post(url=self.url, headers=hdrs, json=self.data)
        return resp


    def PATCH(self):
        hdrs = self.headers.copy()
        hdrs.update({"Content-Type": "application/json"})
        return requests.patch(url=self.url, headers=hdrs, json=self.data)

    def PUT(self):
        pass
 
    def DELETE(self):
        pass


class UsersWrapper(MainWrapper):
    def __init__(self):
        super(UsersWrapper, self).__init__()
        self.url += "users/"

