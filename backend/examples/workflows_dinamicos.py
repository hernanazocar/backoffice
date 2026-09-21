"""
Ejemplos de cómo ejecutar workflows con instrucciones dinámicas
"""
import asyncio
import httpx

async def ejemplo_1_analisis_basico():
    """Análisis normal de competencia"""

    payload = {
        "objetivo": "Crear contenido semanal para redes sociales",
        # El analista usa la configuración por defecto
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/workflows/marketing/run",
            json=payload
        )
        print(response.json())

async def ejemplo_2_analisis_precios_zona():
    """Análisis específico: Precios en una zona particular"""

    payload = {
        "objetivo": "Evaluar precios de la competencia en Zona Norte de Santiago",

        # Instrucciones específicas para el analista
        "instrucciones_analista": {
            "tarea_especial": "evaluar_precios",
            "zona_geografica": "Zona Norte, Santiago, Chile",
            "competidores_especificos": [
                "Líder (supermercado)",
                "Jumbo",
                "Santa Isabel"
            ],
            "productos_a_comparar": [
                "Leche 1L",
                "Pan de molde",
                "Arroz 1kg"
            ],
            "que_buscar": "Busca en web los precios actuales de estos productos en las tiendas de la zona norte"
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/workflows/marketing/run",
            json=payload
        )
        print(response.json())

async def ejemplo_3_analisis_redes_influencers():
    """Análisis específico: Influencers en una industria"""

    payload = {
        "objetivo": "Identificar influencers tech en LATAM para colaboraciones",

        "instrucciones_analista": {
            "tarea_especial": "analizar_influencers",
            "region": "Latinoamérica",
            "industria": "Tecnología / IA",
            "plataforma_principal": "Twitter/X",
            "criterios": {
                "followers_minimos": 10000,
                "engagement_rate_minimo": "2%",
                "temas_relevantes": ["IA", "Machine Learning", "Startups"]
            },
            "influencers_sugeridos": [
                "@usuario1",
                "@usuario2",
                "@usuario3"
            ]
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/workflows/marketing/run",
            json=payload
        )
        print(response.json())

async def ejemplo_4_analisis_sentimiento_marca():
    """Análisis específico: Sentimiento sobre nuestra marca"""

    payload = {
        "objetivo": "Medir sentimiento público sobre nuestra marca en redes",

        "instrucciones_analista": {
            "tarea_especial": "analisis_sentimiento",
            "marca": "Nuestra Empresa",
            "periodo": "últimos 30 días",
            "fuentes": [
                "Twitter menciones",
                "Instagram comentarios",
                "LinkedIn posts",
                "Reddit discussions"
            ],
            "keywords_monitorear": [
                "@nuestraempresa",
                "#nuestrohashtag",
                "nombre producto"
            ],
            "que_analizar": [
                "Sentimiento general (positivo/negativo/neutral)",
                "Temas recurrentes",
                "Quejas principales",
                "Elogios comunes"
            ]
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/workflows/marketing/run",
            json=payload
        )
        print(response.json())

if __name__ == "__main__":
    print("""
    Ejemplos de Workflows Dinámicos
    ================================

    1. Análisis básico de competencia (usa company.json)
    2. Evaluar precios en zona geográfica específica
    3. Identificar influencers para colaboraciones
    4. Medir sentimiento de marca en redes

    Ejecuta cada función para ver ejemplos.
    """)

    # Descomentar para ejecutar:
    # asyncio.run(ejemplo_2_analisis_precios_zona())
