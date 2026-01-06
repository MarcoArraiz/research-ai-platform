import os
import streamlit as st
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env (local)
load_dotenv()

# Desactivar Telemetría para evitar errores de hilos en Streamlit Cloud
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"

class Config:
    """Clase centralizada para manejar la configuración y API Keys."""
    
    def __init__(self):
        # Intentar cargar desde os.environ (.env o Streamlit Secrets)
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        # SerpApi puede venir con dos nombres comunes
        self.SERPAPI_KEY = os.getenv("SERPAPI_KEY") or os.getenv("SERPAPI_API_KEY")
        self.MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")
        
        # Fallback para Streamlit Secrets si os.getenv no funciona en algunos entornos
        try:
            if not self.OPENAI_API_KEY and "OPENAI_API_KEY" in st.secrets:
                self.OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
            if not self.SERPAPI_KEY and "SERPAPI_API_KEY" in st.secrets:
                self.SERPAPI_KEY = st.secrets["SERPAPI_API_KEY"]
            if not self.SERPAPI_KEY and "SERPAPI_KEY" in st.secrets:
                self.SERPAPI_KEY = st.secrets["SERPAPI_KEY"]
        except:
            pass
        
    def validate(self):
        """Valida que las API Keys necesarias estén presentes."""
        errors = []
        if not self.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY no encontrada.")
        if not self.SERPAPI_KEY:
            errors.append("SERPAPI_KEY no encontrada.")
            
        if errors:
            raise ValueError(" | ".join(errors))
        return True

# Instancia global de configuración
config = Config()
