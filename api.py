import datetime
from abc import ABC, abstractmethod

import requests

from models.service_plans import ServicePlan
from models.users import User


class ResponseTypes:
    JsonArray = 'json_array'
    JsonDict = 'json_dict'


class JsonResponse(ABC):
    def __init__(self, response):
        self.response = response
        self.get_data()

    @abstractmethod
    def is_success(self):
        return False

    @abstractmethod
    def get_data(self):
        return None

    @abstractmethod
    def serialize(self, class_name):
        return None


class JsonArrayResponse(JsonResponse):

    def is_success(self):
        return self.response[0] == 0

    def get_data(self):
        return self.response[1]

    def serialize(self, class_name):
        data = self.get_data()
        return [class_name(**item) for item in data]


class JsonDictResponse(JsonResponse):

    def is_success(self):
        return self.response.get('0') == 0

    def get_data(self):
        return self.response.get('1')

    def serialize(self, class_name, append_data=None):
        data = self.get_data()
        if append_data:
            data.update(append_data)
        return class_name(**data)


class JsonResponseFactory:
    @staticmethod
    def create_response(response):
        if isinstance(response, list):
            return JsonArrayResponse(response)
        elif isinstance(response, dict):
            return JsonDictResponse(response)
        else:
            return None


class RMClient:
    def __init__(self, base_url, api_username, api_password):
        self.success_message = None
        self.base_url = base_url
        self.username = api_username
        self.password = api_password

        self.url = None
        self.response = None
        self.json_response = None
        self.is_success = None
        self.data = None

        self.trim_trailing_slash()
        self.generate_full_url()

    def trim_trailing_slash(self):
        if self.base_url.endswith('/'):
            self.base_url = self.base_url[:-1]

    def generate_full_url(self):
        self.url = f"{self.base_url}/api/sysapi.php"

    def get_query_params(self):
        return {
            'apiuser': self.username,
            'apipass': self.password,
        }

    def call_api(self, query_params):
        params = self.get_query_params()
        params.update(query_params)
        response = requests.get(self.url, params=params)
        if not response.content:
            self.is_success = False
            raise ValueError("No response from server")
        self.response = JsonResponseFactory.create_response(response.json())
        if not self.response.is_success():
            self.is_success = False
            raise ValueError(f"Error: {self.response.get_data()}")
        else:
            print(self.success_message)

    def get_all_service_plans(self):
        return self.get_service_plan()

    def get_service_plan(self, service_plan_id=None):
        params = {
            "q": "get_srv",
            "srvid": service_plan_id
        }
        self.success_message = f"Service Plan {service_plan_id} retrieved successfully"
        self.call_api(params)
        self.data = self.response.serialize(ServicePlan)
        return self.data

    def get_user(self, username):
        params = {
            "q": "get_userdata",
            "username": username
        }

        self.success_message = f"User {username} retrieved successfully"
        self.call_api(params)
        user = self.response.serialize(User, append_data={'username': username})
        return user

    def create_user(self,
                    username,
                    password,
                    expiry_date: datetime.date = datetime.date.today(),
                    **kwargs
                    ):

        params = {
            "username": username,
            "password": password,
            "expiry": self.string_date(expiry_date),
        }
        for key, value in kwargs.items():
            params[key] = value
        user = User(**params)
        params.update({"q": "new_user"})
        params.update(user.data_in_rm_format)

        self.success_message = f"User {username} created successfully"
        self.call_api(params)
        return user

    def get_refill_card(self, pin):
        params = {
            "q": "get_refillcard",
            "pin": pin
        }
        self.call_api(params)

        self.success_message = f"Refill card {pin} retrieved successfully"
        self.response.serialize(User)
        return self.data

    def edit_user(self, username, **kwargs):
        params = {
            "q": "edit_user",
            "username": username,
        }
        params.update(kwargs)
        self.success_message = f"User {username} edited successfully"
        self.call_api(params)
        return self.data

    def delete_user(self, username):
        params = {
            "q": "del_user",
            "username": username
        }
        self.success_message = f"User {username} deleted successfully"
        self.call_api(params)
        return self.data

    def disconnect_user(self, username):
        params = {
            "q": "send_pod",
            "username": username
        }
        self.call_api(params)
        return self.data

    def add_credits(self, username, **kwargs):
        params = {
            "q": "add_credits",
            "username": username
        }
        params.update(kwargs)
        self.success_message = f"Credits added successfully to {username}"
        self.call_api(params)
        return self.data

    def get_remaining(self, username):
        params = {
            "q": "get_remaining",
            "username": username
        }
        self.success_message = f"Remaining data for {username} retrieved successfully"
        self.call_api(params)
        return self.data

    @staticmethod
    def string_date(date):
        return date.strftime("%Y-%m-%d")
