import os
from dotenv import load_dotenv


class Helper:
    @staticmethod
    def get_env_variable( name):
        load_dotenv()
        value = os.getenv(name)
        if not value:
            raise ValueError(f"Переменная окружения '{name}' не задана")
        return value

    TOKEN = get_env_variable("TOKEN")
    EMAIL = get_env_variable("EMAIL")
    PASSWORD = get_env_variable("PASSWORD")
    LIST_ID = get_env_variable("LIST_ID")
