import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from crewai.tools import tool

@tool("web_scraper")
def web_scraper(url: str):
    """
    Extrae el contenido de texto principal de una URL dada.
    Detecta automáticamente sitios específicos como SoloTodo para obtener datos en tiempo real.
    """
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        
        # Caso especial para SoloTodo: Usar su API pública para ofertas reales
        clean_url = url.split('?')[0].rstrip('/')
        if "solotodo.cl" in domain and clean_url.endswith(("solotodo.cl", "www.solotodo.cl")):
            api_url = "https://publicapi.solotodo.com/products/browse/?page_size=10&ordering=discount&websites=2"
            api_res = requests.get(api_url, timeout=10)
            if api_res.status_code == 200:
                data = api_res.json()
                results = data.get("results", [])
                output = "Ofertas Reales del Día en SoloTodo:\n"
                for item in results:
                    product = item.get("product", {})
                    name = product.get("name")
                    slug = product.get("slug")
                    id_prod = product.get("id")
                    
                    # Extraer precio y descuento (si están disponibles)
                    entries = item.get("product_entries", [])
                    price_str = "Precio no disponible"
                    if entries:
                        best_entry = entries[0]
                        price = best_entry.get("best_price")
                        if price:
                            price_str = f"${int(float(price)):,}".replace(',', '.')
                    
                    link = f"https://www.solotodo.cl/products/{id_prod}-{slug}"
                    output += f"- {name}: {link} (Precio: {price_str})\n"
                return output

        # Comportamiento general
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }
        response = requests.get(url, headers=headers, timeout=12)
        
        if response.status_code in [403, 401]:
             return f"ACCESS DENIED ({response.status_code}). Do not retry this URL. Immediately search for a different source."

        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Eliminar elementos irrelevantes
        for script_or_style in soup(["script", "style", "nav", "footer", "header", "noscript", "iframe"]):
            script_or_style.decompose()
            
        # Obtener texto y limpiar espacios
        text = soup.get_text(separator=' ')
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        if not text.strip():
            return "El sitio parece ser dinámico y no contiene texto estático legible. Intenta buscar información específica en Google o usa una herramienta de navegación."

        return text[:6000]
        
    except requests.exceptions.Timeout:
        return "The request timed out. Try a different URL or source."
    except Exception as e:
        return f"Error al scrapear la URL {url}: {str(e)}"
