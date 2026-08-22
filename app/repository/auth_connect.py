from supabase import Client

class AuthRepository:
    def __init__(self, client: Client):
        self.client = client

    def sign_up(self, email : str, password: str):
        return self.client.auth.sign_up({"email": email, "password": password})

    def sign_in(self, email : str, password : str):
        return self.client.auth.sign_in_with_password({"email": email, "password":password})

    def get_user_by_id(self, user_id: str):
        return self.client.auth.admin.get_user_by_id(user_id)