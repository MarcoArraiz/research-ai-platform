import os
import sys
from datetime import datetime
from streamlit.runtime.scriptrunner import get_script_run_ctx

# 1. Environment Setup (Critical First Steps)
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from src.utils.config import config
from src.crew.research_crew import ResearchCrew
from src.database.repository import ResearchRepository
from src.ui import components
from src.utils import agent_logic # The new logic helper

# 2. Page Config
st.set_page_config(
    page_title="Elaia Research Platform",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

def save_local_report(topic, content):
    """Backup safe save to local disk."""
    os.makedirs("data/outputs", exist_ok=True)
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{topic.lower().replace(' ', '_')[:30]}.md"
    file_path = os.path.join("data/outputs", filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return file_path

def main():
    components.load_css()
    components.render_sidebar_toggle()
    if st.session_state.get("sidebar_visible", True):
        components.render_sidebar(config)
    components.render_header()
    
    topic = st.text_input("Ingresa un tema para investigar:", placeholder="Ej: El futuro de la desalinización solar en 2026")
    col1, _ = st.columns([1, 4])
    with col1:
        start_research = st.button("🚀 Iniciar Investigación", type="primary")
    if start_research:
        if not topic:
            st.warning("Por favor, ingresa un tema.")
            return
        agent_flow_placeholder = st.empty()
        components.render_agent_visuals(agent_flow_placeholder, "Research Project Coordinator")

        with st.status("🛠️ Agentes trabajando...", expanded=True) as status:
            try:
                st_ctx = get_script_run_ctx()
                def step_callback(step):
                    agent_logic.attach_thread_context(st_ctx)
                    current_role = None
                    if hasattr(step, 'agent'):
                        current_role = getattr(step.agent, 'role', str(step.agent))
        
                    role_key = agent_logic.detect_agent_role(step, current_role)

                    components.render_agent_visuals(agent_flow_placeholder, role_key)
                    
                    if hasattr(step, 'thought') and step.thought:
                        display_name = agent_logic.get_agent_display_name(role_key)
                        status.write(f"💭 **{display_name}**: {step.thought[:150]}...")

                crew = ResearchCrew(topic=topic)
                status.write("🕵️ Iniciando proceso jerárquico...")
                
                result = crew.run(step_callback=step_callback)

                components.render_agent_visuals(agent_flow_placeholder, None)
                status.update(label="✅ Investigación completada!", state="complete", expanded=False)
                
                report_content = str(result)
                if "user" in st.session_state:
                    ResearchRepository.save_research(st.session_state["user"].id, topic, report_content)
                    st.toast("✅ Reporte guardado en la nube")
                saved_path = save_local_report(topic, report_content)
                st.toast(f"Reporte local: {saved_path}")
                st.session_state["current_report"] = report_content
                st.session_state["current_topic"] = topic

            except Exception as e:
                status.update(label="❌ Error crítico", state="error")
                st.error(f"Detalle del error: {str(e)}")

    if "current_report" in st.session_state:
        components.render_final_report(
            st.session_state["current_report"], 
            st.session_state.get("current_topic", "Reporte")
        )
    # Footer
    st.markdown("---")
    st.caption("Investigador Elaia v1.0 | Desarrollado con CrewAI & Streamlit")

if __name__ == "__main__":
    main()