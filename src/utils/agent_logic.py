import threading
from streamlit.runtime.scriptrunner import add_script_run_ctx

def detect_agent_role(step, current_role):
    """
    Heuristic logic to determine which agent is currently acting
    based on the CrewAI step object or thought text.
    """
    # 1. Try explicit role from object
    if current_role and str(current_role) != "None":
        role_str = str(current_role).lower()
        # Normalize role names to match keys in get_agent_display_name
        if "research" in role_str or "investigador" in role_str: return "Senior Research Assistant"
        if "analyst" in role_str or "analista" in role_str: return "Tech Strategy Analyst"
        if "writer" in role_str or "escritor" in role_str or "writing" in role_str: return "Senior Technical Writer"
        if "critic" in role_str or "critico" in role_str: return "Editorial Critic"
        if "coordinator" in role_str or "manager" in role_str: return "Research Project Coordinator"
        return str(current_role) # Fallback to returning the role string itself if no match

    # 2. Analyze thought text if role is ambiguous
    thought_text = getattr(step, 'thought', '').lower()
    
    research_keywords = ["research", "investiga", "search", "google", "scrap", "buscando", "source", "recolect"]
    analysis_keywords = ["analy", "analista", "trend", "tendencia", "impact", "strategic", "risk", "oppor"]
    writing_keywords = ["writ", "escritor", "report", "draft", "markdown", "documento", "summary"]
    critic_keywords = ["critic", "critico", "review", "edit", "feedback", "corrig", "finaliz"]
    
    if any(k in thought_text for k in research_keywords): return "Senior Research Assistant"
    if any(k in thought_text for k in analysis_keywords): return "Tech Strategy Analyst"
    if any(k in thought_text for k in writing_keywords): return "Senior Technical Writer"
    if any(k in thought_text for k in critic_keywords): return "Editorial Critic"
    
    # Default
    return "Research Project Coordinator"

def get_agent_display_name(role_key):
    """Maps technical roles to friendly display names."""
    agent_names = {
        "Research Project Coordinator": "Coordinador", 
        "Senior Research Assistant": "Investigador", 
        "Tech Strategy Analyst": "Analista", 
        "Senior Technical Writer": "Escritor", 
        "Editorial Critic": "Critico"
    }
    return agent_names.get(role_key, "Agente")

def attach_thread_context(st_ctx):
    """Ensures Streamlit context is passed to the thread."""
    if st_ctx:
        add_script_run_ctx(threading.current_thread(), st_ctx)