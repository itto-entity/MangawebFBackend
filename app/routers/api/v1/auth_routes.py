from fastapi import APIRouter, Depends, HTTPException, status
from app.core.supabase import supabase
from app.repository.auth_connect import AuthRepository
from app.repository.profile_repo import ProfileRepository
from app.schemas.auth import (
    TokenResponse,
    UserDetailResponse,
    UserLoginRequest,
    UserRegisterRequest,
)
from app.services.auth_service import AuthServices

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


def get_auth_service() -> AuthServices:
    auth_repo = AuthRepository(client=supabase)
    profile_repo = ProfileRepository(client=supabase)
    return AuthServices(auth_repo=auth_repo, profile_repo=profile_repo)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    payload: UserRegisterRequest,
    service: AuthServices = Depends(get_auth_service),
):
    """
    Register a new user with email, password, and unique username.
    Pydantic validators ensure email format, password length, and clean username.
    """
    try:
        result = service.register_user(payload)
        return {
            "message": "User registered successfully",
            "data": {
                "id": result["user"].id,
                "email": result["user"].email,
                "profile": result["profile"],
            },
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/login", response_model=TokenResponse)
def login(
    payload: UserLoginRequest,
    service: AuthServices = Depends(get_auth_service),
):
    """
    Authenticate user and return session tokens.
    """
    try:
        result = service.login_user(payload)
        session = result.get("session")
        if not session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials or email not confirmed",
            )
        return TokenResponse(
            access_token=session.access_token,
            token_type=session.token_type or "bearer",
            refresh_token=session.refresh_token,
            expires_in=session.expires_in,
            user={
                "id": result["user"].id,
                "email": result["user"].email,
                "profile": result.get("profile"),
            },
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/me/{user_id}", response_model=UserDetailResponse)
def get_current_user_detail(
    user_id: str,
    service: AuthServices = Depends(get_auth_service),
):
    """
    Fetch profile and metadata for a user.
    """
    try:
        user = service.get_full_user(user_id)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found: {str(e)}",
        )
