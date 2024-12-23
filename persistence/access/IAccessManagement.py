"""
this protocol defines the methods exposed
by the identity and access management of the system
"""
from typing import Protocol
from models.UserInfo import UserInfo


class IAccessManagement(Protocol):
    def getToken(username: str, password: str) -> str:
        ...

    def getUser(token: str) -> UserInfo:
        ...

    def registerUser(username: str, password: str, email: str, firstname: str, lastname: str) -> str:
        ...
