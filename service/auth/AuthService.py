from models.UserInfo import UserInfo
from persistence.access import IAccessManagement


class AuthService:
    @staticmethod
    def authenticateUser(username: str, password: str, access: IAccessManagement) -> str:
        """
        validates username and password and returns a token
        Raises:
        AuthenticationError if username and password are not valid
        """
        token = access.getToken(username, password)
        return token

    @staticmethod
    def verifyToken(token: str, access: IAccessManagement) -> UserInfo:
        """
        Verify the given token and return user information.
        Raises:
        InvalidTokenError if token is expired
        AuthenticationError if token is invalid
        """
        userInfo = access.getUser(token)
        return userInfo

    @staticmethod
    def registerUser(username: str, password: str, firstname: str, lastname: str, email: str, access: IAccessManagement) -> str:
        return access.registerUser(username, password, email, firstname, lastname)
