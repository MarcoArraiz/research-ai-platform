from crewai_tools import SerpApiGoogleSearchTool
import os
from src.utils.config import config

def create_search_tool():
    """
    Crea y retorna una herramienta de búsqueda web.
    Utiliza SerpApiGoogleSearchTool si SERPAPI_KEY está configurada.
    """
    if config.SERPAPI_KEY:
        # SerpApiGoogleSearchTool espera la key en os.environ["SERPAPI_API_KEY"]
        os.environ["SERPAPI_API_KEY"] = config.SERPAPI_KEY
        return SerpApiGoogleSearchTool()
    else:
        print("Advertencia: SERPAPI_KEY no configurada. Las herramientas de búsqueda podrían no funcionar.")
        return None
