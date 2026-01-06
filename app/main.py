import os

# CRITICAL: Disable telemetry BEFORE importing any crewai modules to avoid signal error in Streamlit threads
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"

import streamlit as st
import sys
from datetime import datetime

# Añadir el directorio raíz al path para poder importar src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.config import config
from src.crew.research_crew import ResearchCrew

# Configuración de la página
st.set_page_config(
    page_title="AI Research Platform",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para un look "Sobrio" y "Premium"
st.markdown("""
<style>
    .main {
        background-color: transparent;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #1E88E5;
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1565C0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    .report-container {
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        background-color: rgba(255, 255, 255, 0.05);
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

def save_report(topic, content):
    """Guarda el reporte en la carpeta data/outputs."""
    os.makedirs("data/outputs", exist_ok=True)
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{topic.lower().replace(' ', '_')[:30]}.md"
    file_path = os.path.join("data/outputs", filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return file_path

# Sidebar
with st.sidebar:
    st.title("⚙️ Configuración")
    st.info("Plataforma de Investigación con Agentes de IA")
    
    # Selector de Tema Manual
    st.markdown("### 🎨 Apariencia")
    theme_choice = st.radio("Elige un tema:", ["Auto", "Claro", "Oscuro"], horizontal=True)
    
    # CSS dinámico basado en el tema
    if theme_choice == "Claro":
        bg_color = "#FFFFFF"
        text_color = "#31333F"
        border_color = "#e0e0e0"
        report_bg = "rgba(0, 0, 0, 0.02)"
    elif theme_choice == "Oscuro":
        bg_color = "#0E1117"
        text_color = "#FAFAFA"
        border_color = "#3d3d3d"
        report_bg = "rgba(255, 255, 255, 0.05)"
    else: # Auto
        bg_color = "transparent"
        text_color = "inherit"
        border_color = "inherit"
        report_bg = "rgba(128, 128, 128, 0.05)"

    st.markdown(f"""
    <style>
        [data-testid="stAppViewContainer"] {{
            background-color: {bg_color};
            color: {text_color};
        }}
        .report-container {{
            border-color: {border_color};
            background-color: {report_bg};
        }}
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🛠️ Estado del Sistema")
    try:
        config.validate()
        st.success("API Keys: Detectadas")
        
        # Diagnóstico de llaves (enmascaradas)
        with st.expander("Ver diagnóstico"):
            def mask(s): return f"{s[:4]}...{s[-4:]}" if s and len(s) > 8 else "No detectada"
            st.write(f"OpenAI: {mask(config.OPENAI_API_KEY)}")
            st.write(f"SerpApi: {mask(config.SERPAPI_KEY)}")
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
    
    st.markdown("---")
    st.markdown("### 📂 Historial Reciente")
    if os.path.exists("data/outputs"):
        files = sorted(os.listdir("data/outputs"), reverse=True)[:5]
        for f in files:
            st.code(f, language="")

# Main UI
st.title("🔍 Research AI Platform")
st.subheader("Genera reportes técnicos y de mercado en minutos usando agentes autónomos.")

topic = st.text_input("Ingresa un tema para investigar:", placeholder="Ej: El futuro de la desalinización solar en 2026")

col1, col2 = st.columns([1, 4])

with col1:
    start_research = st.button("🚀 Iniciar Investigación")

if start_research:
    if not topic:
        st.warning("Por favor, ingresa un tema.")
    else:
        with st.status("🛠️ Agentes trabajando en la investigación...", expanded=True) as status:
            try:
                # Inicializar Crew
                crew = ResearchCrew(topic=topic)
                
                st.write("🕵️ Researcher buscando fuentes...")
                # Aquí podrías captar stdout si quisieras mostrar logs en tiempo real, 
                # pero para MVP el kickoff directo es más estable.
                result = crew.run()
                
                status.update(label="✅ Investigación completada!", state="complete", expanded=False)
                
                # Convertir resultado a string (CrewAI suele devolver un objeto CrewOutput)
                report_content = str(result)
                
                # Guardar automáticamente (Recomendación del sistema)
                saved_path = save_report(topic, report_content)
                st.toast(f"Reporte guardado en {saved_path}")
                
                # Mostrar Reporte
                st.markdown("---")
                st.header("📄 Reporte Generado")
                st.markdown(f"<div class='report-container'>", unsafe_allow_html=True)
                st.markdown(report_content)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Botón de Descarga
                st.download_button(
                    label="📥 Descargar Reporte (Markdown)",
                    data=report_content,
                    file_name=f"reporte_{topic.lower().replace(' ', '_')}.md",
                    mime="text/markdown"
                )
                
            except Exception as e:
                status.update(label="❌ Error durante la investigación", state="error")
                st.error(f"Ocurrió un error: {str(e)}")

# Footer
st.markdown("---")
st.caption("Investigador de IA v1.0 | Desarrollado con CrewAI & Streamlit")
