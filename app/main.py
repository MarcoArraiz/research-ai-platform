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
from src.database.auth import AuthService
from src.database.repository import ResearchRepository
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx
import threading

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
    .agent-card {
        text-align: center;
        padding: 10px;
        border-radius: 10px;
        transition: all 0.5s ease;
        filter: grayscale(100%);
        opacity: 0.5;
    }
    .agent-active {
        filter: grayscale(0%);
        opacity: 1;
        transform: scale(1.1);
        border: 2px solid #1E88E5;
        box-shadow: 0 0 15px rgba(30, 136, 229, 0.4);
        background-color: rgba(30, 136, 229, 0.1);
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0px rgba(30, 136, 229, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(30, 136, 229, 0); }
        100% { box-shadow: 0 0 0 0px rgba(30, 136, 229, 0); }
    }
    .agent-img {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        margin-bottom: 5px;
        object-fit: cover;
    }
    .agent-name {
        font-size: 0.8rem;
        font-weight: bold;
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
            st.write(f"Supabase URL: {'Detectada' if config.SUPABASE_URL else 'No detectada'}")
            st.write(f"Supabase Key: {mask(config.SUPABASE_KEY)}")
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
    
    st.markdown("---")
    st.markdown("### 👤 Cuenta de Usuario")
    
    if "user" not in st.session_state:
        tab1, tab2 = st.tabs(["Login", "Registro"])
        
        with tab1:
            login_email = st.text_input("Email", key="login_email")
            login_pass = st.text_input("Contraseña", type="password", key="login_pass")
            if st.button("Entrar", key="btn_login"):
                res = AuthService.sign_in(login_email, login_pass)
                if res["error"]:
                    st.error(res["error"])
                else:
                    st.session_state["user"] = res["user"]
                    st.success("¡Bienvenido!")
                    st.rerun()
                    
        with tab2:
            reg_name = st.text_input("Nombre", key="reg_name")
            reg_email = st.text_input("Email", key="reg_email")
            reg_pass = st.text_input("Contraseña", type="password", key="reg_pass")
            if st.button("Registrarse", key="btn_reg"):
                res = AuthService.sign_up(reg_email, reg_pass, reg_name)
                if res["error"]:
                    st.error(res["error"])
                else:
                    st.success("Cuenta creada. Ya puedes iniciar sesión.")
    else:
        user = st.session_state["user"]
        st.write(f"Conectado como: **{user.email}**")
        if st.button("Cerrar Sesión"):
            AuthService.sign_out()
            st.rerun()

    st.markdown("---")
    st.markdown("### 📂 Historial en la Nube")
    if "user" in st.session_state:
        history = ResearchRepository.get_user_history(st.session_state["user"].id)
        if history:
            for item in history[:5]:
                with st.expander(f"📌 {item['topic'][:30]}..."):
                    st.caption(f"Fecha: {item['created_at'][:10]}")
                    if st.button("Cargar Reporte", key=f"load_{item['id']}"):
                        st.session_state["current_report"] = item['result']
                        st.session_state["current_topic"] = item['topic']
        else:
            st.info("No hay investigaciones guardadas.")
    else:
        st.warning("Inicia sesión para ver tu historial.")

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
        # Contenedor para la visualización de agentes
        agent_flow_placeholder = st.empty()
        
        # 1. Definir los roles exactos para el mapeo (deben coincidir con src/agents/*.py)
        ROLE_MAP = {
            "Research Project Coordinator": "Research Project Coordinator",
            "Senior Research Assistant": "Senior Research Assistant",
            "Tech Strategy Analyst": "Tech Strategy Analyst",
            "Senior Technical Writer": "Senior Technical Writer",
            "Editorial Critic": "Editorial Critic"
        }

        # Cache de imágenes base64 para evitar lecturas de disco repetidas
        if "agent_images" not in st.session_state:
            st.session_state["agent_images"] = {}
        
        def get_cached_image_base64(path):
            if path in st.session_state["agent_images"]:
                return st.session_state["agent_images"][path]
            import base64
            try:
                if os.path.exists(path):
                    with open(path, "rb") as f:
                        b64 = base64.b64encode(f.read()).decode()
                        st.session_state["agent_images"][path] = b64
                        return b64
            except: pass
            return ""

        # Redefinir render_agent_flow para usar el cache y roles actualizados
        def render_agent_flow(active_agent_role=None):
            agents = [
                {"role": "Research Project Coordinator", "name": "Coordinador", "img": "app/assets/agents/coordinator.png"},
                {"role": "Senior Research Assistant", "name": "Investigador", "img": "app/assets/agents/researcher.png"},
                {"role": "Tech Strategy Analyst", "name": "Analista", "img": "app/assets/agents/analyst.png"},
                {"role": "Senior Technical Writer", "name": "Escritor", "img": "app/assets/agents/writer.png"},
                {"role": "Editorial Critic", "name": "Critico", "img": "app/assets/agents/critic.png"}
            ]
            
            with agent_flow_placeholder.container():
                cols = st.columns(len(agents))
                for i, agent in enumerate(agents):
                    is_active = active_agent_role == agent["role"]
                    active_class = "agent-active" if is_active else ""
                    with cols[i]:
                        b64 = get_cached_image_base64(agent["img"])
                        st.markdown(f"""
                        <div class="agent-card {active_class}">
                            <img src="data:image/png;base64,{b64}" class="agent-img">
                            <div class="agent-name">{agent["name"]}</div>
                            { "🔵 working..." if is_active else "" }
                        </div>
                        """, unsafe_allow_html=True)

        # Inicializar el flujo con el coordinador
        render_agent_flow("Research Project Coordinator")

        with st.status("🛠️ Agentes trabajando en la investigación...", expanded=True) as status:
            try:
                # 1. Callback de Tarea (al finalizar cada tarea principal)
                def task_callback(task_output):
                    pass # Seguimiento granual via step_callback

                # Asegurar que los callbacks tengan el contexto de Streamlit si CrewAI usa hilos
                st_ctx = get_script_run_ctx()

                # 3. Callback de paso (granual, cada vez que un agente piensa o actúa)
                def step_callback(step):
                    # Vincular el hilo actual al contexto de Streamlit del usuario
                    if st_ctx:
                        add_script_run_ctx(threading.current_thread(), st_ctx)
                    
                    # Intentar extraer el rol del agente del objeto step
                    current_role = None
                    if hasattr(step, 'agent'):
                        agent_obj = step.agent
                        if hasattr(agent_obj, 'role'):
                            current_role = agent_obj.role
                        else:
                            current_role = str(agent_obj)
                    
                    # Heurística para Hierarchical Process: Si el rol es 'None' o Manager,
                    # intentamos detectar si se refiere a un agente específico en el pensamiento.
                    thought_text = getattr(step, 'thought', '').lower()
                    found_role_key = None

                    # Primero buscar coincidencia en el rol (más flexible)
                    if current_role and str(current_role) != "None":
                        role_str = str(current_role).lower()
                        if "research" in role_str or "investigador" in role_str:
                            found_role_key = "Senior Research Assistant"
                        elif "analyst" in role_str or "analista" in role_str:
                            found_role_key = "Tech Strategy Analyst"
                        elif "writer" in role_str or "escritor" in role_str or "writing" in role_str:
                            found_role_key = "Senior Technical Writer"
                        elif "critic" in role_str or "critico" in role_str:
                            found_role_key = "Editorial Critic"
                        elif "coordinator" in role_str or "manager" in role_str:
                            found_role_key = "Research Project Coordinator"
                    
                    # Si no hay match claro en el rol, buscar pistas profundas en el pensamiento
                    if not found_role_key and thought_text:
                        # Palabras clave expandidas por rol
                        research_keywords = ["research", "investiga", "search", "google", "scrap", "buscando", "source", "recolect"]
                        analysis_keywords = ["analy", "analista", "trend", "tendencia", "impact", "strategic", "risk", "oppor"]
                        writing_keywords = ["writ", "escritor", "report", "draft", "markdown", "documento", "summary"]
                        critic_keywords = ["critic", "critico", "review", "edit", "feedback", "corrig", "finaliz"]
                        
                        if any(k in thought_text for k in research_keywords):
                            found_role_key = "Senior Research Assistant"
                        elif any(k in thought_text for k in analysis_keywords):
                            found_role_key = "Tech Strategy Analyst"
                        elif any(k in thought_text for k in writing_keywords):
                            found_role_key = "Senior Technical Writer"
                        elif any(k in thought_text for k in critic_keywords):
                            found_role_key = "Editorial Critic"
                    
                    # Si seguimos sin nada o es el manager orquestando, por defecto es el Coordinador
                    if not found_role_key:
                        found_role_key = "Research Project Coordinator"

                    # Actualizar UI
                    render_agent_flow(found_role_key)
                    
                    # Escribir el pensamiento actual en el log
                    if hasattr(step, 'thought') and step.thought:
                        # Buscar el nombre bonito
                        agent_names = {
                            "Research Project Coordinator": "Coordinador", 
                            "Senior Research Assistant": "Investigador", 
                            "Tech Strategy Analyst": "Analista", 
                            "Senior Technical Writer": "Escritor", 
                            "Editorial Critic": "Critico"
                        }
                        display_name = agent_names.get(found_role_key, "Agente")
                        status.write(f"💭 **{display_name}**: {step.thought[:150]}...")
                
                # Inicializar Crew
                crew = ResearchCrew(topic=topic)
                
                status.write("🕵️ El Coordinador está iniciando el proceso jerárquico...")
                render_agent_flow("Research Project Coordinator")
                
                # Ejecutar investigación con ambos callbacks
                result = crew.run(task_callback=task_callback, step_callback=step_callback)
                
                render_agent_flow(None) # Limpiar al terminar
                status.update(label="✅ Investigación completada!", state="complete", expanded=False)
                
                # Convertir resultado a string
                report_content = str(result)
                
                # Persistencia en Supabase si el usuario está logueado
                if "user" in st.session_state:
                    ResearchRepository.save_research(st.session_state["user"].id, topic, report_content)
                    st.toast("✅ Reporte guardado en la nube")
                
                # Guardar localmente
                saved_path = save_report(topic, report_content)
                st.toast(f"Reporte guardado en {saved_path}")
                
                # Almacenar en session_state para persistencia de la interfaz
                st.session_state["current_report"] = report_content
                st.session_state["current_topic"] = topic
                
            except Exception as e:
                status.update(label="❌ Error durante la investigación", state="error")
                st.error(f"Ocurrió un error: {str(e)}")

# Mostrar Reporte si existe (Fuera de los bloques de procesamiento para persistencia)
if "current_report" in st.session_state:
    report_content = st.session_state["current_report"]
    topic_rendered = st.session_state.get("current_topic", "Reporte")
    
    st.markdown("---")
    st.header(f"📄 Reporte: {topic_rendered}")
    st.markdown(f"<div class='report-container'>", unsafe_allow_html=True)
    st.markdown(report_content)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.download_button(
        label="📥 Descargar Reporte (Markdown)",
        data=report_content,
        file_name=f"reporte_{topic_rendered.lower().replace(' ', '_')}.md",
        mime="text/markdown"
    )

# Footer
st.markdown("---")
st.caption("Investigador de IA v1.0 | Desarrollado con CrewAI & Streamlit")
