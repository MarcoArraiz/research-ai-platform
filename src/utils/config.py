import os
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
load_dotenv()

class Config:
    """Clase centralizada para manejar la configuración y API Keys."""
    
    def __init__(self):
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.SERPAPI_KEY = os.getenv("SERPAPI_KEY")
        self.MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")
        
    def validate(self):
        """Valida que las API Keys necesarias estén presentes."""
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY no encontrada en el entorno.")
        return True

# Instancia global de configuración
config = Config()
