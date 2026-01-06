from crewai_tools import SerperDevTool
import os
from src.utils.config import config

def create_search_tool():
    """
    Crea y retorna una herramienta de búsqueda web.
    Utiliza SerperDevTool si SERPAPI_KEY está configurada.
    """
    if config.SERPAPI_KEY:
        # Asegurarse de que la variable de entorno que espera crewai_tools esté seteada
        os.environ["SERPER_API_KEY"] = config.SERPAPI_KEY
        return SerperDevTool()
    else:
        # Por ahora, si no hay key, retornamos None (o podríamos implementar un fallback)
        print("Advertencia: SERPAPI_KEY no configurada. Las herramientas de búsqueda podrían no funcionar.")
        return None
