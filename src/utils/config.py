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
        # 1. Intentar cargar desde os.environ (Variables de sistema o .env)
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.SERPAPI_KEY = os.getenv("SERPAPI_KEY") or os.getenv("SERPAPI_API_KEY")
        self.MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")
        self.SUPABASE_URL = os.getenv("SUPABASE_URL")
        self.SUPABASE_KEY = os.getenv("SUPABASE_KEY")
        
        # 2. Fallback para Streamlit Secrets (Producción en Streamlit Cloud)
        try:
            if not self.OPENAI_API_KEY and "OPENAI_API_KEY" in st.secrets:
                self.OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
            if not self.SERPAPI_KEY:
                if "SERPAPI_API_KEY" in st.secrets:
                    self.SERPAPI_KEY = st.secrets["SERPAPI_API_KEY"]
                elif "SERPAPI_KEY" in st.secrets:
                    self.SERPAPI_KEY = st.secrets["SERPAPI_KEY"]
            if not self.SUPABASE_URL and "SUPABASE_URL" in st.secrets:
                self.SUPABASE_URL = st.secrets["SUPABASE_URL"]
            if not self.SUPABASE_KEY and "SUPABASE_KEY" in st.secrets:
                self.SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
        except:
            # st.secrets no está disponible localmente si no hay .streamlit/secrets.toml
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
