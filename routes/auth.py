"""
contains mappings for auth flow
:author Muhammad Rowaha<ashfaqrowaha@gmail.com>
"""
from fastapi import APIRouter, FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from dto.token import TokenResponse
from dto.login import LoginDto
from dto.register import RegisterDto, RegisterRespDto
from models.UserInfo import UserInfo

from persistence.access import IAccessManagement
from persistence.injectors import getAccessManagement
from persistence.access.exceptions import UserAlreadyExistsError

from service.auth import AuthService
router = APIRouter(prefix="/auth")
bearer_scheme = HTTPBearer()


@router.post("/register", response_model=RegisterRespDto, status_code=status.HTTP_201_CREATED)
async def registerUser(
    register: RegisterDto,
    access: IAccessManagement = Depends(getAccessManagement)
):
    try:
        userId = AuthService.registerUser(
            register.username,
            register.password,
            register.firstname,
            register.lastname,
            register.email,
            access
        )
        return RegisterRespDto(userId=userId)
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user name already exists"
        )


@router.post("/login", response_model=TokenResponse)
async def login(login: LoginDto, access: IAccessManagement = Depends(getAccessManagement)):
    try:
        print(login)
        access_token = AuthService.authenticateUser(
            login.username, login.password, access)
        return TokenResponse(access_token=access_token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )


@router.get("/me", response_model=UserInfo)
async def protected_endpoint(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    access: IAccessManagement = Depends(getAccessManagement)
):
    """
    Protected endpoint that requires a valid token for access.

    Args:
        credentials (HTTPAuthorizationCredentials): Bearer token provided via HTTP Authorization header.

    Returns:
        UserInfo: Information about the authenticated user.
    """
    token = credentials.credentials
    try:
        userInfo = AuthService.verifyToken(token, access)
        return userInfo
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def register(app: FastAPI, *, prefix: str) -> None:
    global router
    app.include_router(router, prefix=prefix)
