import requests
from bs4 import BeautifulSoup
from crewai.tools import tool

@tool("web_scraper")
def web_scraper(url: str):
    """
    Extrae el contenido de texto principal de una URL dada.
    Útil cuando necesitas profundizar en la información de un sitio web específico
    después de haberlo encontrado en una búsqueda.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Eliminar elementos irrelevantes
        for script_or_style in soup(["script", "style", "nav", "footer", "header"]):
            script_or_style.decompose()
            
        # Obtener texto y limpiar espacios
        text = soup.get_text(separator='\n')
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        # Limitar a los primeros 4000 caracteres para evitar saturar el contexto
        return text[:4000]
        
    except Exception as e:
        return f"Error al scrapear la URL {url}: {str(e)}"
