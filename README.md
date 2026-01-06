# 🔍 Research AI Platform

Plataforma SaaS de investigación de mercado impulsada por agentes de Inteligencia Artificial colectivos (CrewAI). Genera reportes exhaustivos en minutos en lugar de semanas.

## 🚀 Características
- **Multi-Agentes**: Un equipo de 5 agentes especializados (Researcher, Analyst, Writer, Critic).
- **Búsqueda en Tiempo Real**: Integración con Google Search vía SerpApi.
- **Sober UI**: Interfaz profesional desarrollada en Streamlit con soporte para Modo Oscuro/Claro.
- **Auto-Guardado**: Todos los reportes se almacenan automáticamente en Markdown.

## 🛠️ Instalación Local

1. **Clonar el repositorio:**
   ```bash
   git clone <tu-repo-url>
   cd research-ai-platform
   ```

2. **Crear y activar entorno virtual:**
   ```bash
   python -m venv venv
   # En Windows:
   source venv/Scripts/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno:**
   Crea un archivo `.env` basado en `.env.example`:
   ```env
   OPENAI_API_KEY=tu_key_aqui
   SERPAPI_API_KEY=tu_key_aqui
   ```

5. **Correr la aplicación:**
   ```bash
   streamlit run app/main.py
   ```

## 🌐 Despliegue en la Nube
Para desplegar en **Streamlit Cloud**:
1. Sube este código a GitHub.
2. Conecta tu repo en [share.streamlit.io](https://share.streamlit.io).
3. Configura los **Secrets** con las mismas variables del `.env`.

## 📄 Licencia
MIT
