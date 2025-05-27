import json
from urllib.request import urlopen

from Config import *
from Exceptions import *


class APIHandler:
    def make_request(self, method, parameters):
        request = REQUEST_TEMPLATE.format(
            method=method,
            parameters=parameters,
            VERSION=VERSION,
            ACCESS_TOKEN=ACCESS_TOKEN
        )
        with urlopen(request) as url:
            response = json.loads(url.read())
        return response

    def get_user(self, user_id):
        response = self.make_request("users.get", f"user_ids={user_id}")
        return response

    def get_user_id(self, user_id):
        user = self.get_user(user_id)
        if not user["response"]:
            raise InvalidIdException(f"Person {user_id} does not exist")
        return self.get_user(user_id)["response"][0]["id"]

    def get_user_full_name(self, user_id):
        user = self.get_user(user_id)
        if not user["response"]:
            raise InvalidIdException(f"Person {user_id} does not exist")
        first_name = user["response"][0]["first_name"]
        last_name = user["response"][0]["last_name"]
        return first_name, last_name
