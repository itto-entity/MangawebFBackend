from app.core.config import settings
from supabase import create_client, Client

SUPABASE_URL = settings.supabase_url
SUPABASE_ANON_KEY  = settings.supabase_anon_key
SUPABASE_ROLE_KEY = settings.supabase_role_key

supabase : Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
supabase_admin: Client = create_client(SUPABASE_URL, SUPABASE_ROLE_KEY)