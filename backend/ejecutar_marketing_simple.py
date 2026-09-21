#!/usr/bin/env python3
"""
Script simple para ejecutar el equipo de Marketing
Genera posts de ejemplo en modo MOCK
"""
import os
import json
import time
from datetime import datetime
import sys

# Agregar el directorio backend al path
sys.path.insert(0, os.path.dirname(__file__))

def crear_directorio_si_no_existe(path):
    """Crea un directorio si no existe"""
    os.makedirs(path, exist_ok=True)

def generar_posts_ejemplo():
    """Genera 7 posts de ejemplo"""
    posts = [
        {
            "id": f"post_{int(time.time())}_{i}",
            "titulo": titulo,
            "copy": copy,
            "plataformas": plataformas,
            "horario_sugerido": "15:00",
            "hashtags": hashtags,
            "fecha_creacion": datetime.now().isoformat(),
            "estado": "pending"
        }
        for i, (titulo, copy, plataformas, hashtags) in enumerate([
            (
                "Lanzamiento Producto Q4",
                "🚀 ¡Descubre nuestra nueva línea de productos diseñada especialmente para impulsar tu negocio! Características premium que transformarán tu forma de trabajar. #Innovación #Productividad",
                ["instagram", "facebook"],
                ["#Innovación", "#Productividad", "#NuevoProducto"]
            ),
            (
                "Tips de Productividad",
                "💡 5 formas de mejorar tu productividad hoy:\n\n1. Organiza tu espacio de trabajo\n2. Establece objetivos claros\n3. Toma descansos regulares\n4. Usa herramientas adecuadas\n5. Revisa tu progreso\n\n¿Cuál aplicarás primero?",
                ["linkedin", "twitter"],
                ["#Productividad", "#Tips", "#Empresa"]
            ),
            (
                "Testimonial de Cliente",
                '⭐⭐⭐⭐⭐\n\n"Gracias a esta herramienta logramos aumentar nuestras ventas en 40% en solo 3 meses. El equipo está encantado con los resultados."\n\n- María González, CEO de Tech Solutions\n\n¿Quieres resultados similares?',
                ["instagram", "linkedin"],
                ["#Testimonial", "#Resultados", "#Clientes"]
            ),
            (
                "Estadística del Sector",
                "📊 Dato del día:\n\n78% de las empresas que implementan automatización reportan un aumento significativo en eficiencia.\n\n¿Tu empresa ya está automatizando procesos?\n\n#DatoDelDía #Automatización",
                ["linkedin", "twitter"],
                ["#Estadísticas", "#Automatización", "#Empresa"]
            ),
            (
                "Behind the Scenes",
                "👨‍💻 Detrás de cámaras:\n\nAsí trabaja nuestro equipo para brindarte la mejor experiencia. Innovación, dedicación y pasión por lo que hacemos.\n\n¿Quieres conocer más sobre nosotros?",
                ["instagram", "facebook"],
                ["#BehindTheScenes", "#Equipo", "#Cultura"]
            ),
            (
                "Oferta Especial",
                "🎁 ¡OFERTA ESPECIAL POR TIEMPO LIMITADO!\n\n30% de descuento en todos nuestros planes durante esta semana.\n\nCódigo: PROMO30\n\n⏰ Oferta válida hasta el viernes\n\n¡No te lo pierdas!",
                ["instagram", "facebook", "twitter"],
                ["#Oferta", "#Descuento", "#Promoción"]
            ),
            (
                "Pregunta Interactiva",
                "🤔 Pregunta del día:\n\n¿Cuál es el mayor desafío que enfrentas en tu negocio?\n\nA) Gestión del tiempo\nB) Generación de leads\nC) Automatización de procesos\nD) Análisis de datos\n\nComéntanos tu respuesta 👇",
                ["instagram", "linkedin"],
                ["#Pregunta", "#Interacción", "#Comunidad"]
            )
        ])
    ]
    return posts

def guardar_posts(posts, directorio):
    """Guarda los posts en archivos JSON"""
    for post in posts:
        archivo = os.path.join(directorio, f"{post['id']}.json")
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(post, f, indent=2, ensure_ascii=False)
        print(f"  ✓ Post guardado: {post['titulo']}")

def main():
    print("\n" + "="*60)
    print("🚀 EJECUTANDO EQUIPO DE MARKETING")
    print("="*60)

    # Crear directorios necesarios
    base_dir = os.path.join(os.path.dirname(__file__), '..', 'posts')
    pending_dir = os.path.join(base_dir, 'pending')

    print("\n📁 Creando directorios...")
    crear_directorio_si_no_existe(pending_dir)

    # Simular trabajo de cada agente
    print("\n👥 AGENTES TRABAJANDO:\n")

    agentes = [
        ("Gerente de Marketing", "Coordinando estrategia general"),
        ("Market Intelligence", "Analizando mercado y competencia"),
        ("Community Manager", "Creando contenido para RRSS"),
        ("Growth Specialist", "Generando estrategias de leads"),
        ("Diseñador Gráfico", "Creando piezas visuales"),
        ("Analista de Marketing", "Generando reportes de métricas")
    ]

    for nombre, actividad in agentes:
        print(f"  🤖 {nombre}: {actividad}")
        time.sleep(0.5)

    # Generar posts
    print("\n📝 Generando posts...")
    posts = generar_posts_ejemplo()

    # Guardar posts
    print(f"\n💾 Guardando {len(posts)} posts en: {pending_dir}")
    guardar_posts(posts, pending_dir)

    print("\n" + "="*60)
    print("✅ WORKFLOW COMPLETADO EXITOSAMENTE")
    print("="*60)
    print(f"\n📊 RESUMEN:")
    print(f"  • Posts creados: {len(posts)}")
    print(f"  • Estado: Pendientes de aprobación")
    print(f"  • Ubicación: posts/pending/")
    print(f"\n💡 Ve al dashboard → Marketing → RRSS para aprobar los posts")
    print("\n")

if __name__ == "__main__":
    main()
