from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    database_url : str
    minutes : int = 30
    supabase_anon_key : str
    supabase_role_key : str
    supabase_url : str
    storage_bucket : str = "manga-assets"
    storage_signed_url_expires_in : int = 3600
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )
settings = Settings()
