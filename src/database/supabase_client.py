import os
from supabase import create_client, Client
from src.utils.config import config

def get_supabase_client() -> Client:
    """
    Inicializa y retorna el cliente de Supabase.
    """
    url = config.SUPABASE_URL
    key = config.SUPABASE_KEY
    
    if not url or not key:
        raise ValueError("SUPABASE_URL y SUPABASE_KEY deben estar configuradas.")
        
    return create_client(url, key)

# Cliente singleton para uso general
try:
    supabase: Client = get_supabase_client()
except Exception as e:
    print(f"Advertencia: No se pudo conectar a Supabase: {str(e)}")
    supabase = None
