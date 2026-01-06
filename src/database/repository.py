from typing import List, Dict, Any, Optional
from src.database.supabase_client import supabase

class ResearchRepository:
    """Clase para manejar la persistencia de investigaciones en la base de datos."""

    @staticmethod
    def save_research(user_id: str, topic: str, result: str) -> Dict[str, Any]:
        """Guarda un reporte de investigación en la tabla 'researches'."""
        try:
            data = {
                "user_id": user_id,
                "topic": topic,
                "result": result,
                "status": "completed"
            }
            response = supabase.table("researches").insert(data).execute()
            return {"data": response.data, "error": None}
        except Exception as e:
            return {"data": None, "error": str(e)}

    @staticmethod
    def get_user_history(user_id: str) -> List[Dict[str, Any]]:
        """Obtiene el historial de investigaciones de un usuario específico."""
        try:
            response = supabase.table("researches") \
                .select("*") \
                .eq("user_id", user_id) \
                .order("created_at", desc=True) \
                .execute()
            return response.data
        except Exception as e:
            print(f"Error al obtener historial: {str(e)}")
            return []

    @staticmethod
    def get_research_by_id(research_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene una investigación específica por su ID."""
        try:
            response = supabase.table("researches") \
                .select("*") \
                .eq("id", research_id) \
                .single() \
                .execute()
            return response.data
        except Exception as e:
            print(f"Error al obtener investigación: {str(e)}")
            return None
