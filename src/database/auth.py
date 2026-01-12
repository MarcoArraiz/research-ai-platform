import logging
from typing import Optional, Dict, Any
from src.database.supabase_client import supabase
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuthService:
    """Servicio para manejar la autenticación con Supabase."""

    @staticmethod
    def sign_up(email: str, password: str, name: str) -> Dict[str, Any]:
        """Registra un nuevo usuario."""
        try:
            # 1. Crear usuario en Supabase Auth
            # La creación del registro en la tabla 'public.users' se maneja vía Trigger en Supabase
            response = supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "full_name": name
                    }
                }
            })
            
            if response.user:
                logger.info(f"Usuario registrado exitosamente: {email}")
            
            return {"user": response.user, "error": None}
        except Exception as e:
            logger.error(f"Error en sign_up: {str(e)}")
            return {"user": None, "error": str(e)}

    @staticmethod
    def sign_in(email: str, password: str) -> Dict[str, Any]:
        """Inicia sesión de un usuario existente."""
        try:
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            logger.info(f"Inicio de sesión exitoso: {email}")
            return {"user": response.user, "session": response.session, "error": None}
        except Exception as e:
            logger.error(f"Error en sign_in: {str(e)}")
            return {"user": None, "error": str(e)}

    @staticmethod
    def sign_out():
        """Cierra la sesión actual."""
        try:
            supabase.auth.sign_out()
            if "user" in st.session_state:
                del st.session_state["user"]
            logger.info("Sesión cerrada")
        except Exception as e:
            logger.error(f"Error al cerrar sesión: {str(e)}")

    @staticmethod
    def get_user():
        """Retorna el usuario actual de la sesión."""
        try:
            return supabase.auth.get_user()
        except:
            return None
