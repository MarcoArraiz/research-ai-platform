import streamlit as st
import sass
import os
import base64
from src.database.auth import AuthService
from src.database.repository import ResearchRepository

def load_css():
    scss_file = os.path.join(os.path.dirname(__file__), "styles.scss")
    try:
        with open(scss_file, 'r') as f:
            css_content = sass.compile(string=f.read())
        st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error compiling styles: {e}")

def get_cached_image_base64(path):
    if "agent_images" not in st.session_state:
        st.session_state["agent_images"] = {}
    
    if path in st.session_state["agent_images"]:
        return st.session_state["agent_images"][path]
    
    try:
        if os.path.exists(path):
            with open(path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                st.session_state["agent_images"][path] = b64
                return b64
    except: pass
    return ""

def render_header():
    st.title("🔍 Elaia Research AI Platform")
    st.subheader("Genera reportes técnicos y de mercado en minutos usando agentes autónomos.")

def render_sidebar(config):
    
    """Handles the entire Sidebar: Theme, Auth, History."""
    with st.sidebar:
        st.title("⚙️ Configuración")
        st.info("Plataforma de Investigación con Agentes de IA")
        
        # --- Theme Selector ---
        st.markdown("### 🎨 Apariencia")
        theme_choice = st.radio("Elige un tema:", ["Auto", "Claro", "Oscuro"], horizontal=True, key="theme_selector")
        _apply_theme_css(theme_choice)
        
        st.markdown("---")
        
        # --- System Status ---
        st.markdown("### 🛠️ Estado del Sistema")
        try:
            config.validate()
            st.success("API Keys: Detectadas")
            with st.expander("Ver diagnóstico"):
                def mask(s): return f"{s[:4]}...{s[-4:]}" if s and len(s) > 8 else "No detectada"
                st.write(f"OpenAI: {mask(config.OPENAI_API_KEY)}")
                st.write(f"SerpApi: {mask(config.SERPAPI_KEY)}")
                st.write(f"Supabase: {'Conectado' if config.SUPABASE_URL else 'Error'}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
        
        st.markdown("---")
        
        # --- Auth Logic ---
        st.markdown("### 👤 Cuenta de Usuario")
        _render_auth_section()

        st.markdown("---")
        
        # --- History ---
        st.markdown("### 📂 Historial")
        _render_history_section()


def render_sidebar_toggle():
    """
    Renderiza un botón personalizado para mostrar/ocultar el sidebar
    y aplica el CSS necesario según el estado.
    """
    if "sidebar_visible" not in st.session_state:
        st.session_state["sidebar_visible"] = True

    if not st.session_state["sidebar_visible"]:
        st.markdown("""
            <style>
                section[data-testid="stSidebar"] {
                    display: none !important;
                }
                /* Ajustar el margen del contenido principal para que ocupe todo el ancho */
                .main .block-container {
                    max-width: 100% !important;
                    padding-left: 5rem !important;
                }
            </style>
        """, unsafe_allow_html=True)
    col1, col2 = st.columns([0.5, 10])
    with col1:
        icon = "◀️" if st.session_state["sidebar_visible"] else "▶️"
        if st.button(icon, key="sidebar_toggle_btn", help="Mostrar/Ocultar Menú"):
            st.session_state["sidebar_visible"] = not st.session_state["sidebar_visible"]
            st.rerun()
            
def _apply_theme_css(theme_choice):
    """Internal helper to apply dynamic colors."""
    if theme_choice == "Claro":
        bg, text, border, r_bg = "#FFFFFF", "#31333F", "#e0e0e0", "rgba(0,0,0,0.02)"
    elif theme_choice == "Oscuro":
        bg, text, border, r_bg = "#0E1117", "#FAFAFA", "#3d3d3d", "rgba(255,255,255,0.05)"
    else:
        bg, text, border, r_bg = "transparent", "inherit", "inherit", "rgba(128,128,128,0.05)"

    st.markdown(f"""
    <style>
        [data-testid="stAppViewContainer"] {{ background-color: {bg}; color: {text}; }}
        .report-container {{ border-color: {border}; background-color: {r_bg}; }}
    </style>
    """, unsafe_allow_html=True)

def _render_auth_section():
    if "user" not in st.session_state:
        tab1, tab2 = st.tabs(["Login", "Registro"])
        with tab1:
            email = st.text_input("Email", key="l_mail")
            pwd = st.text_input("Pass", type="password", key="l_pass")
            if st.button("Entrar"):
                res = AuthService.sign_in(email, pwd)
                if res["error"]: st.error(res["error"])
                else: 
                    st.session_state["user"] = res["user"]
                    st.success("¡Bienvenido!")
                    st.rerun()
        with tab2:
            name = st.text_input("Nombre", key="r_name")
            email = st.text_input("Email", key="r_email")
            pwd = st.text_input("Pass", type="password", key="r_pass")
            if st.button("Registrarse"):
                res = AuthService.sign_up(email, pwd, name)
                if res["error"]: st.error(res["error"])
                else: st.success("Cuenta creada.")
    else:
        st.write(f"Conectado: **{st.session_state['user'].email}**")
        if st.button("Cerrar Sesión"):
            AuthService.sign_out()
            st.rerun()

def _render_history_section():
    if "user" in st.session_state:
        history = ResearchRepository.get_user_history(st.session_state["user"].id)
        if history:
            for item in history[:5]:
                with st.expander(f"📌 {item['topic'][:30]}..."):
                    st.caption(f"Fecha: {item['created_at'][:10]}")
                    if st.button("Cargar", key=f"load_{item['id']}"):
                        st.session_state["current_report"] = item['result']
                        st.session_state["current_topic"] = item['topic']
        else:
            st.info("No hay investigaciones.")
    else:
        st.warning("Inicia sesión para ver historial.")

def render_agent_visuals(placeholder, active_role=None):
    """Renders the horizontal list of agents with active state."""
    agents = [
        {"role": "Research Project Coordinator", "name": "Coordinador", "img": "app/assets/agents/coordinator.png"},
        {"role": "Senior Research Assistant", "name": "Investigador", "img": "app/assets/agents/researcher.png"},
        {"role": "Tech Strategy Analyst", "name": "Analista", "img": "app/assets/agents/analyst.png"},
        {"role": "Senior Technical Writer", "name": "Escritor", "img": "app/assets/agents/writer.png"},
        {"role": "Editorial Critic", "name": "Critico", "img": "app/assets/agents/critic.png"}
    ]
    
    with placeholder.container():
        cols = st.columns(len(agents))
        for i, agent in enumerate(agents):
            is_active = active_role == agent["role"]
            active_class = "agent-active" if is_active else ""
            
            with cols[i]:
                b64 = get_cached_image_base64(agent["img"])
                # Fallback icon if image missing
                img_tag = f'<img src="data:image/png;base64,{b64}" class="agent-img">' if b64 else '<div style="font-size:30px">🤖</div>'
                
                st.markdown(f"""
                <div class="agent-card {active_class}">
                    {img_tag}
                    <div class="agent-name">{agent["name"]}</div>
                    { "<div class='pulsing-dot'></div>" if is_active else "" }
                </div>
                """, unsafe_allow_html=True)

def render_final_report(content, topic):
    st.markdown("---")
    st.header(f"📄 Reporte: {topic}")
    st.markdown(f"<div class='report-container'>", unsafe_allow_html=True)
    st.markdown(content)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.download_button(
        label="📥 Descargar Reporte (Markdown)",
        data=content,
        file_name=f"reporte_{topic.lower().replace(' ', '_')[:30]}.md",
        mime="text/markdown"
    )