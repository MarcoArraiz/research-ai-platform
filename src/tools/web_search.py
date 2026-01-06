from crewai_tools import SerpApiGoogleSearchTool
import os
from src.utils.config import config

def create_search_tool():
    """
    Crea y retorna una herramienta de búsqueda web.
    """
    print("DEBUG: Creando herramienta de búsqueda (SerpApi)...")
    if config.SERPAPI_KEY:
        try:
            os.environ["SERPAPI_API_KEY"] = config.SERPAPI_KEY
            tool = SerpApiGoogleSearchTool()
            print("DEBUG: Herramienta de búsqueda creada exitosamente.")
            return tool
        except Exception as e:
            print(f"DEBUG ERROR: Falló la creación de la herramienta: {str(e)}")
            return None
    else:
        print("DEBUG: No se encontró SERPAPI_KEY.")
        return None
