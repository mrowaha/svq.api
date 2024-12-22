from pydantic_settings import BaseSettings
from pydantic import Field
from keycloak import KeycloakOpenID, KeycloakAdmin
from keycloak.exceptions import KeycloakAuthenticationError, KeycloakPostError
from ..exceptions import AuthenticationError, InvalidTokenError, UserAlreadyExistsError
from models.UserInfo import UserInfo


class KeyCloakSettings(BaseSettings):
    keycloak_server_url: str = Field(..., env="KEYCLOAK_SERVER_URL")
    keycloak_realm: str = Field(..., env="KEYCLOAK_REALM")
    keycloak_client_id: str = Field(..., env="KEYCLOAK_CLIENT_ID")
    keycloak_client_secret: str = Field(..., env="KEYCLOAK_CLIENT_SECRET")
    keycloak_username: str = Field(..., env="KEYCLOAK_USERNAME")
    keycloak_password: str = Field(..., env="KEYCLOAY_PASSWORD")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"


class KeyCloakAccessManagement:
    """
    implements IAccessManagement
    """

    def __init__(self):
        self.settings: KeyCloakSettings = KeyCloakSettings()
        self.client = KeycloakOpenID(
            server_url=self.settings.keycloak_server_url,
            realm_name=self.settings.keycloak_realm,
            client_id=self.settings.keycloak_client_id,
            client_secret_key=self.settings.keycloak_client_secret,
        )
        print(self.settings)
        self.adminClient = KeycloakAdmin(
            server_url=self.settings.keycloak_server_url,
            username=self.settings.keycloak_username,
            password=self.settings.keycloak_password,
            realm_name=self.settings.keycloak_realm,
            client_id=self.settings.keycloak_client_id,
            client_secret_key=self.settings.keycloak_client_secret,
        )

    def getToken(self: "KeyCloakAccessManagement", username: str, password: str) -> str:
        try:
            token = self.client.token(username, password)
            return token["access_token"]
        except KeycloakAuthenticationError as e:
            raise AuthenticationError()

    def getUser(self: "KeyCloakAccessManagement", token: str) -> UserInfo:
        try:
            userInfo = self.client.userinfo(token)
            if not userInfo:
                raise InvalidTokenError()

            return UserInfo(
                preferred_username=userInfo["preferred_username"],
                email=userInfo.get("email"),
                full_name=userInfo.get("name"),
            )
        except KeycloakAuthenticationError:
            raise AuthenticationError()

    def registerUser(
        self: "KeyCloakAccessManagement",
        username: str,
        password: str,
        email: str,
        firstname: str,
        lastname: str,
    ) -> str:
        """
        Registers a new user in Keycloak.
        """
        try:
            user_id = self.adminClient.create_user(
                {
                    "username": username,
                    "email": email,
                    "enabled": True,
                    "firstName": firstname,
                    "lastName": lastname,
                    "credentials": [{"type": "password", "value": password, "temporary": False}],
                }
            )
            return user_id
        except KeycloakPostError:
            raise UserAlreadyExistsError()


keyCloakClient = KeyCloakAccessManagement()


def getKeyCloakClient() -> KeyCloakAccessManagement:
    return keyCloakClient
