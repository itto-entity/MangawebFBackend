from typing import Any, Dict
from app.repository.auth_connect import AuthRepository
from app.repository.profile_repo import ProfileRepository
from app.schemas.auth import UserLoginRequest, UserRegisterRequest


class AuthServices:
    def __init__(self, auth_repo: AuthRepository, profile_repo: ProfileRepository):
        self.auth_repo = auth_repo
        self.profile_repo = profile_repo

    def register_user(self, payload: UserRegisterRequest) -> Dict[str, Any]:
        auth_res = self.auth_repo.sign_up(payload.email, payload.password)
        user_id = str(auth_res.user.id)

        profile = self.profile_repo.create_profile(user_id, payload.username)

        return {
            "user": auth_res.user,
            "profile": profile,
            "session": auth_res.session,
        }

    def login_user(self, payload: UserLoginRequest) -> Dict[str, Any]:
        auth_res = self.auth_repo.sign_in(payload.email, payload.password)
        user_id = str(auth_res.user.id)
        profile_data = self.profile_repo.get_profile_by_id(user_id)

        return {
            "user": auth_res.user,
            "session": auth_res.session,
            "profile": profile_data,
        }

    def get_full_user(self, user_id: str) -> Dict[str, Any]:
        auth_data = self.auth_repo.get_user_by_id(user_id)
        profile_data = self.profile_repo.get_profile_by_id(user_id)

        return {
            "id": user_id,
            "email": auth_data.user.email if hasattr(auth_data, "user") else None,
            "username": profile_data.get("username") if profile_data else None,
            "role": profile_data.get("role", "member") if profile_data else "member",
            "avatar_url": profile_data.get("avatar_url") if profile_data else None,
        }