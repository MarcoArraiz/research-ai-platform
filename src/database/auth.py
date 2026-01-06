from typing import Optional, Dict, Any
from src.database.supabase_client import supabase
import streamlit as st

class AuthService:
    """Servicio para manejar la autenticación con Supabase."""

    @staticmethod
    def sign_up(email: str, password: str, name: str) -> Dict[str, Any]:
        """Registra un nuevo usuario."""
        try:
            # 1. Crear usuario en Supabase Auth
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
                # 2. Crear entrada en nuestra tabla de users (el trigger de Supabase podría automatizar esto, 
                # pero lo hacemos explícito para asegurar sincronía inicial)
                supabase.table("users").upsert({
                    "id": response.user.id,
                    "email": email,
                    "name": name
                }).execute()
                
            return {"user": response.user, "error": None}
        except Exception as e:
            return {"user": None, "error": str(e)}

    @staticmethod
    def sign_in(email: str, password: str) -> Dict[str, Any]:
        """Inicia sesión de un usuario existente."""
        try:
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            return {"user": response.user, "session": response.session, "error": None}
        except Exception as e:
            return {"user": None, "error": str(e)}

    @staticmethod
    def sign_out():
        """Cierra la sesión actual."""
        try:
            supabase.auth.sign_out()
            if "user" in st.session_state:
                del st.session_state["user"]
        except Exception as e:
            print(f"Error al cerrar sesión: {str(e)}")

    @staticmethod
    def get_user():
        """Retorna el usuario actual de la sesión."""
        try:
            return supabase.auth.get_user()
        except:
            return None
