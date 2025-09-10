import json
import requests

from src.data.json_convert import JsonConvert
from src.enums.headers import Header
from src.enums.urls import Url
from src.enums.static_ids import StaticId
from utils.helpers import Helper


class ClickupApi:
    HEADERS = {Header.AUTHORIZATION.value: Helper.TOKEN,
        Header.ACCEPT.value: Header.JSON.value,
        Header.CONTENT_TYPE.value: Header.JSON.value}

    def __init__(self):
        self.headers = self.HEADERS
        self.url = Url.API_URL.value

    def get_tasks(self, list_id=StaticId.LIST_ID.value, **query_params):
        url = f"{self.url.rstrip("/")}/api/v2/list/{list_id}/task"
        response = requests.get(url=url, params=query_params, headers=self.headers)
        self.__log(response)
        return response

    def create_task(self, data, list_id=StaticId.LIST_ID.value):
        url = f"{self.url.rstrip("/")}/api/v2/list/{list_id}/task"
        response = requests.post(url=url, json=JsonConvert.data_to_json(data), headers=self.headers)
        self.__log(response)
        return response

    def get_task(self, task_id, **query_params):
        url = f"{self.url.rstrip("/")}/api/v2/task/{task_id}"
        response = requests.get(url=url, params=query_params, headers=self.headers)
        self.__log(response)
        return response

    def update_task(self, task_id, data=None, **query_params):
        url = f"{self.url.rstrip("/")}/api/v2/task/{task_id}"
        response = requests.put(url=url, params=query_params, json=JsonConvert.data_to_json(data), headers=self.headers)
        self.__log(response)
        return response

    def delete_task(self, task_id, **query_params):
        url = f"{self.url.rstrip("/")}/api/v2/task/{task_id}"
        response = requests.delete(url=url, params=query_params, headers=self.headers)
        self.__log(response)
        return response

    def __log(self, response):
        logs = f"\n========== REQUEST =========="
        logs += f"\nURL: {response.request.url}"
        logs += f"\nMethod: {response.request.method}"
        logs += f"\nHeaders: {response.request.headers}"
        if response.request.body:
            try:
                logs += f"\nBody: {json.dumps(json.loads(response.request.body), indent=2)}"
            except:
                logs += f"\nBody: {response.request.body}"
        logs += f"\n========== RESPONSE =========="
        logs += f"\nStatus: {response.status_code}"
        if response.content:
            logs += f"\nResponse: {json.dumps(json.loads(response.text), indent=2, ensure_ascii=False)}"
        else:
            logs += "\nResponse:<empty>"
        logs += "\n================================================================================\n"
        print(logs)
