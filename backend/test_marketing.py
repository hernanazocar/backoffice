"""
Script de prueba para ejecutar el workflow de Marketing
"""
import asyncio
import httpx
import json
from datetime import datetime

async def test_marketing_workflow():
    """Probar el workflow completo de marketing"""

    base_url = "http://localhost:8000"

    print("🧪 Probando Sistema de Agentes IA - Marketing")
    print("=" * 60)

    async with httpx.AsyncClient(timeout=300.0) as client:

        # 1. Verificar que el servidor esté corriendo
        print("\n1️⃣ Verificando servidor...")
        try:
            response = await client.get(f"{base_url}/")
            print(f"✅ Servidor: {response.json()['message']}")
        except Exception as e:
            print(f"❌ Error: No se puede conectar al servidor")
            print(f"   Asegúrate de que el servidor esté corriendo: python main.py")
            return

        # 2. Ver agentes disponibles
        print("\n2️⃣ Consultando agentes disponibles...")
        response = await client.get(f"{base_url}/api/agents/status")
        agents = response.json()
        print(f"✅ {len(agents)} agentes encontrados:")
        for agent in agents:
            print(f"   • {agent['name']} ({agent['department']}) - {agent['status']}")

        # 3. Ejecutar workflow de marketing
        print("\n3️⃣ Ejecutando workflow de Marketing...")
        print("   (Esto puede tomar varios minutos...)")

        payload = {
            "objetivo": "Crear estrategia de contenido para el lanzamiento de nuestro nuevo producto 'Agentes IA Pro'",
            "contexto": {
                "producto": "Plataforma de agentes IA para empresas",
                "publico_objetivo": "CEOs y directores de tecnología",
                "canales": ["LinkedIn", "Twitter", "Instagram"]
            }
        }

        try:
            response = await client.post(
                f"{base_url}/api/workflows/marketing/run",
                json=payload
            )

            result = response.json()

            if result.get("success"):
                print("\n✅ Workflow completado exitosamente!")
                print("\n📊 RESULTADOS:")
                print("=" * 60)

                final_state = result.get("results", {})

                # Mostrar resultados de cada agente
                sections = [
                    ("📈 Análisis del Analista", "analisis_competencia"),
                    ("📝 Grilla de Community Manager", "grilla_contenido"),
                    ("🎨 Diseños Orgánicos", "diseños_organicos"),
                    ("💰 Campañas de Paid Media", "campañas_creadas"),
                    ("🎨 Diseños Paid", "diseños_paid"),
                    ("📤 Publicaciones Realizadas", "posts_publicados"),
                    ("📊 Reporte Final", "reporte")
                ]

                for title, key in sections:
                    value = final_state.get(key, "")
                    if value:
                        print(f"\n{title}:")
                        print("-" * 60)
                        # Mostrar primeros 500 caracteres
                        preview = value[:500] + "..." if len(value) > 500 else value
                        print(preview)

                # Mensajes del sistema
                messages = final_state.get("messages", [])
                if messages:
                    print("\n📋 Log de Actividades:")
                    print("-" * 60)
                    for msg in messages:
                        print(f"  {msg}")

                # Errores si los hay
                errors = final_state.get("errors", [])
                if errors:
                    print("\n⚠️  Errores encontrados:")
                    for error in errors:
                        print(f"  {error}")

            else:
                print("\n❌ Error en el workflow:")
                print(json.dumps(result, indent=2))

        except Exception as e:
            print(f"\n❌ Error ejecutando workflow: {str(e)}")

        # 4. Ver historial de ejecuciones
        print("\n4️⃣ Consultando historial de ejecuciones...")
        response = await client.get(f"{base_url}/api/workflows/executions?limit=5")
        executions = response.json()
        print(f"✅ Últimas {len(executions)} ejecuciones:")
        for ex in executions:
            status_emoji = "✅" if ex['status'] == 'completed' else "❌"
            print(f"   {status_emoji} {ex['workflow_name']} - {ex['status']} ({ex['started_at']})")

        # 5. Ver actividades recientes
        print("\n5️⃣ Consultando actividades recientes...")
        response = await client.get(f"{base_url}/api/activities?limit=10")
        activities = response.json()
        print(f"✅ Últimas {len(activities)} actividades:")
        for act in activities[:5]:  # Mostrar solo las 5 más recientes
            print(f"   • {act['agent']} ({act['department']}): {act['action']}")

    print("\n" + "=" * 60)
    print("✅ Prueba completada!")
    print("\n💡 Tip: Revisa el dashboard en http://localhost:3001")

if __name__ == "__main__":
    asyncio.run(test_marketing_workflow())
