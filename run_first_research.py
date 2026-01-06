from src.crew.research_crew import ResearchCrew
import os
import sys

def main():
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = "Tendencias de IA Generativa en 2026"
    
    print(f"🚀 Iniciando investigación sobre: {topic}...")
    
    # Asegurar que el directorio de salida existe
    os.makedirs("data/outputs", exist_ok=True)
    
    crew = ResearchCrew(topic=topic)
    result = crew.run()
    
    print("\n" + "="*50)
    print("RESULTADO DE LA INVESTIGACIÓN:")
    print("="*50)
    print(result)
    
    # Guardar resultado en un archivo markdown
    # Limpiar nombre de archivo si tiene espacios
    filename = topic.lower().replace(" ", "_")[:50] + ".md"
    output_path = os.path.join("data/outputs", filename)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(str(result))
    
    print(f"\n✅ Reporte guardado en: {output_path}")

if __name__ == "__main__":
    main()
