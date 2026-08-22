from supabase import Client

class ProfileRepository:
    def __init__(self, client: Client):
        self.client = client

    def create_profile(self, user_id: str, username: str):
        response = self.client.table("profiles").insert({
            "id": user_id,
            "username": username
        }).execute()
        return response.data

    def get_profile_by_id(self, user_id: str):
        response = self.client.table("profiles").select("*").eq("id", user_id).single().execute()
        return response.data