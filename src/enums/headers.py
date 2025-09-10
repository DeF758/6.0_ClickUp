from enum import Enum


class Header(Enum):
    AUTHORIZATION: str = "Authorization"
    ACCEPT: str = "accept"
    CONTENT_TYPE: str = "Content-Type"
    JSON: str = "application/json"
