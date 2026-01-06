import os
from crewai.tools import tool
from serpapi import GoogleSearch
from src.utils.config import config

@tool("google_search")
def google_search(query: str):
    """
    Realiza una búsqueda en Google usando SerpApi y retorna los resultados.
    Útil para encontrar noticias actuales, tendencias y datos técnicos.
    """
    print(f"DEBUG: Ejecutando custom google_search para: {query}")
    try:
        search = GoogleSearch({
            "q": query,
            "api_key": config.SERPAPI_KEY,
            "num": 5
        })
        results = search.get_dict()
        
        # Extraer solo los snippets de los resultados orgánicos
        organic_results = results.get("organic_results", [])
        if not organic_results:
            return "No se encontraron resultados relevantes."
            
        formatted_results = []
        for res in organic_results[:5]:
            title = res.get("title")
            link = res.get("link")
            snippet = res.get("snippet")
            formatted_results.append(f"Título: {title}\nLink: {link}\nResumen: {snippet}\n---")
            
        return "\n".join(formatted_results)
    except Exception as e:
        return f"Error al realizar la búsqueda: {str(e)}"

def create_search_tool():
    """
    Retorna la función de búsqueda decorada como herramienta para CrewAI.
    """
    print("DEBUG: Retornando custom tool de búsqueda...")
    if config.SERPAPI_KEY:
        return google_search
    else:
        print("DEBUG: No se encontró SERPAPI_KEY para la custom tool.")
        return None
