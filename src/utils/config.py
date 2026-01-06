import os
import streamlit as st
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env (local)
load_dotenv()

# Desactivar Telemetría de todas las formas posibles antes de cargarCrewAI
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"
os.environ["TELEMETRY_ENABLED"] = "false"
os.environ["ANONYMIZED_TELEMETRY"] = "false"

class Config:
    """Clase centralizada para manejar la configuración y API Keys."""
    
    def __init__(self):
        # Intentar cargar desde os.environ (.env o Streamlit Secrets)
        self.SUPABASE_URL = os.getenv("SUPABASE_URL")
        self.SUPABASE_KEY = os.getenv("SUPABASE_KEY")
        
        # Fallback para Streamlit Secrets si os.getenv no funciona en algunos entornos
        try:
            if not self.OPENAI_API_KEY and "OPENAI_API_KEY" in st.secrets:
                self.OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
            if not self.SERPAPI_KEY and "SERPAPI_API_KEY" in st.secrets:
                self.SERPAPI_KEY = st.secrets["SERPAPI_API_KEY"]
            if not self.SERPAPI_KEY and "SERPAPI_KEY" in st.secrets:
                self.SERPAPI_KEY = st.secrets["SERPAPI_KEY"]
            if not self.SUPABASE_URL and "SUPABASE_URL" in st.secrets:
                self.SUPABASE_URL = st.secrets["SUPABASE_URL"]
            if not self.SUPABASE_KEY and "SUPABASE_KEY" in st.secrets:
                self.SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
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
