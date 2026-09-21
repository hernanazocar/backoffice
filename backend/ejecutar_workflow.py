#!/usr/bin/env python3
"""
Script para ejecutar workflows con instrucciones específicas
"""
import asyncio
import httpx
import json

# URL del backend (asegúrate que esté corriendo en http://localhost:8000)
API_URL = "http://localhost:8000"

async def ejecutar_workflow_basico():
    """
    EJEMPLO 1: Análisis básico de competencia
    Usa la configuración de company.json
    """
    print("\n" + "="*60)
    print("🚀 EJECUTANDO: Análisis Básico de Competencia")
    print("="*60)

    payload = {
        "objetivo": "Crear contenido semanal para redes sociales"
    }

    print("\n📤 Enviando request...")
    print(f"Payload: {json.dumps(payload, indent=2)}")

    async with httpx.AsyncClient(timeout=300.0) as client:
        try:
            response = await client.post(
                f"{API_URL}/api/workflows/marketing/run",
                json=payload
            )

            result = response.json()

            if result.get("success"):
                print("\n✅ WORKFLOW COMPLETADO!")
                print(f"\n📊 REPORTE FINAL:")
                print(result.get("results", {}).get("reporte", "No hay reporte"))
            else:
                print(f"\n❌ ERROR: {result}")

        except Exception as e:
            print(f"\n❌ Error conectando al backend: {str(e)}")
            print("\n💡 Asegúrate de que el backend esté corriendo:")
            print("   cd backend && python main.py")

async def ejecutar_workflow_precios_zona():
    """
    EJEMPLO 2: Análisis de precios en zona específica
    Instrucciones dinámicas personalizadas
    """
    print("\n" + "="*60)
    print("💰 EJECUTANDO: Análisis de Precios por Zona")
    print("="*60)

    payload = {
        "objetivo": "Comparar precios de supermercados en Zona Norte de Santiago",

        # 🎯 AQUÍ VAN LAS INSTRUCCIONES ESPECÍFICAS
        "instrucciones_analista": {
            "tarea_especial": "evaluar_precios",
            "zona_geografica": "Zona Norte, Santiago, Chile",
            "competidores_a_analizar": [
                "Líder (sucursal Independencia)",
                "Jumbo (Mall Plaza Norte)",
                "Unimarc (Huechuraba)"
            ],
            "productos_a_comparar": [
                {
                    "nombre": "Leche Colun 1 Litro",
                    "categoria": "Lácteos"
                },
                {
                    "nombre": "Pan Ideal",
                    "categoria": "Panadería"
                },
                {
                    "nombre": "Arroz Grado 1 1kg",
                    "categoria": "Abarrotes"
                }
            ],
            "que_buscar": [
                "Precio actual de cada producto en cada tienda",
                "Promociones vigentes",
                "Disponibilidad en sucursales de la zona"
            ],
            "como_buscar": "Usa web_search() para buscar en los sitios web de cada supermercado. Busca precios específicos de la zona norte."
        }
    }

    print("\n📤 Enviando request...")
    print(f"Payload: {json.dumps(payload, indent=2, ensure_ascii=False)}")

    async with httpx.AsyncClient(timeout=300.0) as client:
        try:
            response = await client.post(
                f"{API_URL}/api/workflows/marketing/run",
                json=payload
            )

            result = response.json()

            if result.get("success"):
                print("\n✅ ANÁLISIS DE PRECIOS COMPLETADO!")
                print(f"\n📊 RESULTADOS:")

                # Mostrar análisis del analista
                analisis = result.get("results", {}).get("analisis_competencia", "")
                if analisis:
                    print("\n" + "-"*60)
                    print("ANÁLISIS DEL ANALISTA:")
                    print("-"*60)
                    print(analisis[:1000])  # Primeros 1000 caracteres

            else:
                print(f"\n❌ ERROR: {result}")

        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

async def ejecutar_workflow_influencers():
    """
    EJEMPLO 3: Identificar influencers para colaboraciones
    """
    print("\n" + "="*60)
    print("👥 EJECUTANDO: Análisis de Influencers Tech")
    print("="*60)

    payload = {
        "objetivo": "Identificar influencers tech en LATAM para colaboraciones",

        "instrucciones_analista": {
            "tarea_especial": "analizar_influencers",
            "region": "Latinoamérica",
            "industria": "Tecnología / Inteligencia Artificial",
            "plataforma_principal": "Twitter/X",
            "criterios_seleccion": {
                "followers_minimos": 10000,
                "engagement_rate_minimo": "2%",
                "idioma": "Español",
                "temas_relevantes": [
                    "Inteligencia Artificial",
                    "Machine Learning",
                    "Startups",
                    "Desarrollo de Software"
                ]
            },
            "influencers_sugeridos_investigar": [
                "@influencer1",
                "@influencer2",
                "@influencer3"
            ],
            "que_analizar": [
                "Número de seguidores y engagement",
                "Temas que publican",
                "Frecuencia de publicación",
                "Tipo de audiencia",
                "Potencial para colaboración"
            ]
        }
    }

    print("\n📤 Enviando request...")
    print(f"Objetivo: {payload['objetivo']}")

    async with httpx.AsyncClient(timeout=300.0) as client:
        try:
            response = await client.post(
                f"{API_URL}/api/workflows/marketing/run",
                json=payload
            )

            result = response.json()
            print(f"\n✅ Resultado: {result.get('status', 'unknown')}")

        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

# ============================================================
# MENÚ PRINCIPAL
# ============================================================

async def menu():
    """Menú interactivo para elegir qué workflow ejecutar"""

    print("\n" + "="*60)
    print("🤖 SISTEMA DE AGENTES IA - EJECUTAR WORKFLOWS")
    print("="*60)

    print("\nSelecciona qué workflow ejecutar:\n")
    print("1. Análisis básico de competencia (usa company.json)")
    print("2. Comparar precios por zona (ejemplo: Zona Norte Santiago)")
    print("3. Identificar influencers tech para colaboraciones")
    print("4. Salir")

    opcion = input("\nElige opción (1-4): ")

    if opcion == "1":
        await ejecutar_workflow_basico()
    elif opcion == "2":
        await ejecutar_workflow_precios_zona()
    elif opcion == "3":
        await ejecutar_workflow_influencers()
    elif opcion == "4":
        print("\n👋 Saliendo...")
        return False
    else:
        print("\n❌ Opción inválida")

    return True

async def main():
    """Función principal"""
    print("\n🚀 Iniciando sistema...")

    # Verificar que el backend esté corriendo
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_URL}/")
            print(f"✅ Backend conectado: {response.json()['message']}")
    except Exception as e:
        print(f"\n❌ ERROR: No se puede conectar al backend en {API_URL}")
        print("\n💡 Para iniciar el backend:")
        print("   cd /Users/hernanazocar/agentes-org/backend")
        print("   source venv/bin/activate")
        print("   python main.py")
        print("\n   Luego ejecuta este script nuevamente.")
        return

    # Mostrar menú
    while True:
        continuar = await menu()
        if not continuar:
            break

        input("\n\nPresiona Enter para continuar...")

if __name__ == "__main__":
    asyncio.run(main())
