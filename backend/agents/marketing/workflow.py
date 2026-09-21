from typing import Dict, Any, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from agents.marketing.team import (
    analista_marketing,
    community_manager,
    diseñador_grafico,
    paid_media,
    reportador_marketing
)
from loguru import logger
import operator

class MarketingState(TypedDict):
    """Estado del flujo de trabajo de marketing"""
    # Input inicial
    objetivo: str
    fecha_inicio: str

    # Outputs de Analista
    analisis_competencia: str
    directrices_contenido: str
    insights_paid_media: str

    # Outputs de Community Manager
    grilla_contenido: str
    copy_posts: str
    posts_publicados: str

    # Outputs de Diseñador
    diseños_organicos: str
    diseños_paid: str

    # Outputs de Paid Media
    campañas_creadas: str

    # Reporte final
    reporte: str

    # Metadata
    messages: Annotated[list, operator.add]
    errors: Annotated[list, operator.add]

async def analista_node(state: MarketingState) -> Dict:
    """Nodo 1: Analista revisa redes y competencia"""
    logger.info("🔍 Analista iniciando análisis...")

    task = {
        "title": "Análisis de Redes Sociales y Competencia",
        "description": f"""
        Objetivo: {state['objetivo']}

        Tareas:
        1. Revisa nuestras redes sociales actuales
        2. Analiza la comunicación digital de la competencia
        3. Identifica tendencias y oportunidades
        4. Define directrices de contenido para el Community Manager
        5. Proporciona insights para campañas de Paid Media
        """,
        "context": f"Fecha de inicio: {state['fecha_inicio']}"
    }

    result = await analista_marketing.execute(task)

    if result['status'] == 'completed':
        output = result['output']
        return {
            "analisis_competencia": output,
            "directrices_contenido": output,
            "insights_paid_media": output,
            "messages": [f"✅ Analista completó análisis"]
        }
    else:
        return {
            "errors": [f"❌ Error en Analista: {result.get('error')}"],
            "messages": [f"❌ Analista falló"]
        }

async def community_grilla_node(state: MarketingState) -> Dict:
    """Nodo 2: Community Manager crea grilla y copy"""
    logger.info("📝 Community Manager creando grilla...")

    task = {
        "title": "Crear Grilla de Contenido y Copy",
        "description": f"""
        Basándote en las directrices del analista:

        {state['directrices_contenido']}

        Tareas:
        1. Crea una grilla de contenido para la semana
        2. Escribe el copy para cada publicación
        3. Define formatos y tono para cada pieza
        """,
        "input_data": {
            "directrices": state['directrices_contenido']
        }
    }

    result = await community_manager.execute(task)

    if result['status'] == 'completed':
        return {
            "grilla_contenido": result['output'],
            "copy_posts": result['output'],
            "messages": [f"✅ Community Manager creó grilla y copy"]
        }
    else:
        return {
            "errors": [f"❌ Error en Community Manager: {result.get('error')}"],
            "messages": [f"❌ Community Manager falló"]
        }

async def diseñador_organico_node(state: MarketingState) -> Dict:
    """Nodo 3: Diseñador crea diseños orgánicos"""
    logger.info("🎨 Diseñador creando diseños orgánicos...")

    task = {
        "title": "Crear Diseños para Contenido Orgánico",
        "description": f"""
        Basándote en la grilla de contenido:

        {state['grilla_contenido']}

        Tareas:
        1. Crea diseños visuales para cada publicación de la grilla
        2. Asegúrate de que sean consistentes con la marca
        3. Optimiza para cada red social (Instagram, Facebook, LinkedIn, etc.)
        4. Entrega archivos listos para publicar
        """,
        "input_data": {
            "grilla": state['grilla_contenido'],
            "copy": state['copy_posts']
        }
    }

    result = await diseñador_grafico.execute(task)

    if result['status'] == 'completed':
        return {
            "diseños_organicos": result['output'],
            "messages": [f"✅ Diseñador completó diseños orgánicos"]
        }
    else:
        return {
            "errors": [f"❌ Error en Diseñador: {result.get('error')}"],
            "messages": [f"❌ Diseñador falló"]
        }

async def paid_media_node(state: MarketingState) -> Dict:
    """Nodo 4 (paralelo): Paid Media crea campañas"""
    logger.info("💰 Paid Media creando campañas...")

    task = {
        "title": "Crear Campañas de Paid Media",
        "description": f"""
        Basándote en los insights del analista:

        {state['insights_paid_media']}

        Tareas:
        1. Define estrategia de campañas pagadas
        2. Crea audiencias objetivo
        3. Define presupuestos y pujas
        4. Especifica creatividades necesarias para el diseñador
        5. Configura campañas en plataformas (Meta Ads, Google Ads)
        """,
        "input_data": {
            "insights": state['insights_paid_media']
        }
    }

    result = await paid_media.execute(task)

    if result['status'] == 'completed':
        return {
            "campañas_creadas": result['output'],
            "messages": [f"✅ Paid Media creó campañas"]
        }
    else:
        return {
            "errors": [f"❌ Error en Paid Media: {result.get('error')}"],
            "messages": [f"❌ Paid Media falló"]
        }

async def diseñador_paid_node(state: MarketingState) -> Dict:
    """Nodo 5: Diseñador crea diseños para paid"""
    logger.info("🎨 Diseñador creando diseños para campañas...")

    task = {
        "title": "Crear Diseños para Campañas Pagadas",
        "description": f"""
        Basándote en las especificaciones de Paid Media:

        {state['campañas_creadas']}

        Tareas:
        1. Crea diseños para cada campaña
        2. Optimiza para conversión
        3. Crea variantes A/B testing
        4. Entrega en formatos requeridos por cada plataforma
        """,
        "input_data": {
            "campañas": state['campañas_creadas']
        }
    }

    result = await diseñador_grafico.execute(task)

    if result['status'] == 'completed':
        return {
            "diseños_paid": result['output'],
            "messages": [f"✅ Diseñador completó diseños paid"]
        }
    else:
        return {
            "errors": [f"❌ Error en Diseñador Paid: {result.get('error')}"],
            "messages": [f"❌ Diseñador Paid falló"]
        }

async def community_publicar_node(state: MarketingState) -> Dict:
    """Nodo 6: Community Manager publica contenido"""
    logger.info("📤 Community Manager publicando contenido...")

    task = {
        "title": "Publicar Contenido en Redes Sociales",
        "description": f"""
        Diseños listos:
        {state['diseños_organicos']}

        Tareas:
        1. Programa las publicaciones en cada red social
        2. Monitorea las primeras interacciones
        3. Responde comentarios iniciales
        4. Confirma que todo está publicado correctamente
        """,
        "input_data": {
            "diseños": state['diseños_organicos'],
            "copy": state['copy_posts']
        }
    }

    result = await community_manager.execute(task)

    if result['status'] == 'completed':
        return {
            "posts_publicados": result['output'],
            "messages": [f"✅ Community Manager publicó contenido"]
        }
    else:
        return {
            "errors": [f"❌ Error publicando: {result.get('error')}"],
            "messages": [f"❌ Publicación falló"]
        }

async def reportador_node(state: MarketingState) -> Dict:
    """Nodo 7: Reportador genera reporte para Gerente"""
    logger.info("📊 Reportador generando reporte...")

    task = {
        "title": "Generar Reporte para Gerente de Marketing",
        "description": f"""
        Genera un reporte completo consolidando:

        1. Análisis realizado: {state.get('analisis_competencia', 'N/A')}
        2. Contenido creado: {state.get('grilla_contenido', 'N/A')}
        3. Diseños producidos: {state.get('diseños_organicos', 'N/A')}
        4. Publicaciones realizadas: {state.get('posts_publicados', 'N/A')}
        5. Campañas configuradas: {state.get('campañas_creadas', 'N/A')}

        El reporte debe incluir:
        - Resumen ejecutivo
        - Métricas clave
        - Recomendaciones
        - Próximos pasos
        """,
        "input_data": {
            "todas_actividades": state.get('messages', [])
        }
    }

    result = await reportador_marketing.execute(task)

    if result['status'] == 'completed':
        return {
            "reporte": result['output'],
            "messages": [f"✅ Reportador generó reporte final"]
        }
    else:
        return {
            "errors": [f"❌ Error en Reportador: {result.get('error')}"],
            "messages": [f"❌ Reportador falló"]
        }

# Construir el grafo de workflow
def create_marketing_workflow():
    """Crear el flujo de trabajo de marketing"""

    workflow = StateGraph(MarketingState)

    # Agregar nodos
    workflow.add_node("analista", analista_node)
    workflow.add_node("community_grilla", community_grilla_node)
    workflow.add_node("diseñador_organico", diseñador_organico_node)
    workflow.add_node("paid_media", paid_media_node)
    workflow.add_node("diseñador_paid", diseñador_paid_node)
    workflow.add_node("community_publicar", community_publicar_node)
    workflow.add_node("reportador", reportador_node)

    # Definir flujo
    workflow.set_entry_point("analista")

    # Flujo principal: Analista → Community (grilla) → Diseñador (orgánico) → Community (publicar)
    workflow.add_edge("analista", "community_grilla")
    workflow.add_edge("community_grilla", "diseñador_organico")
    workflow.add_edge("diseñador_organico", "community_publicar")

    # Flujo paralelo: Analista → Paid Media → Diseñador (paid)
    workflow.add_edge("analista", "paid_media")
    workflow.add_edge("paid_media", "diseñador_paid")

    # Ambos flujos convergen en reportador
    workflow.add_edge("community_publicar", "reportador")
    workflow.add_edge("diseñador_paid", "reportador")

    # Fin
    workflow.add_edge("reportador", END)

    return workflow.compile()
