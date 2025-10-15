import os
from datetime import datetime

from dotenv import load_dotenv


class Helper:
    @staticmethod
    def get_env_variable(name):
        load_dotenv()
        value = os.getenv(name)
        if not value:
            raise ValueError(f"Переменная окружения '{name}' не задана")
        return value

    TOKEN = get_env_variable("TOKEN")
    EMAIL = get_env_variable("EMAIL")
    PASSWORD = get_env_variable("PASSWORD")
    LIST_ID = get_env_variable("LIST_ID")

    @staticmethod
    def choice_field(field_name: str, get_gen_data):
        match field_name.lower():
            case "name":
                return {field_name: get_gen_data.name}
            case "description":
                return {"name": get_gen_data.name, "description": get_gen_data.description}
            case "assignees":
                return {"name": get_gen_data.name, "assignees": get_gen_data.assignees}
            case "archived":
                return {"name": get_gen_data.name, "archived": get_gen_data.archived}
            case "tags":
                return {"name": get_gen_data.name, "tags": get_gen_data.tags}
            case "status":
                return {"name": get_gen_data.name, "status": get_gen_data.status}
            case "priority":
                return {"name": get_gen_data.name, "priority": get_gen_data.priority}
            case "due_date":
                return {"name": get_gen_data.name, "due_date": get_gen_data.due_date}
            case "start_date":
                return {"name": get_gen_data.name, "start_date": get_gen_data.start_date}

    @staticmethod
    def unix_conv(date: str) -> int:
        '''"dd/mm/yyyy" or "dd/mm/yyyy hh:mm:ss"'''
        try:
            dt = datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            dt = datetime.strptime(date, "%d/%m/%Y %H:%M:%S")
        epoch = datetime(1970,1,1)
        return int((dt-epoch).total_seconds() * 1000)
