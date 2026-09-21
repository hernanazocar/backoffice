from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime
import asyncio
import json

from database.connection import init_db, get_db
from database import models
from agents.marketing.workflow import create_marketing_workflow
from loguru import logger
import os
from dotenv import load_dotenv

load_dotenv()

# Inicializar FastAPI
app = FastAPI(
    title="Agentes IA - Backend API",
    description="Sistema de orquestación de agentes IA para gestión empresarial",
    version="1.0.0"
)

# CORS
origins = json.loads(os.getenv("CORS_ORIGINS", '["http://localhost:3001","http://localhost:8000"]'))
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket manager para actualizaciones en tiempo real
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

# Inicializar base de datos
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Iniciando sistema de agentes...")
    init_db()
    logger.info("✅ Base de datos inicializada")

    # Crear datos iniciales si no existen
    db = next(get_db())
    if db.query(models.Department).count() == 0:
        await seed_database(db)
    logger.info("✅ Sistema listo")

async def seed_database(db: Session):
    """Crear datos iniciales"""
    logger.info("📊 Creando datos iniciales...")

    # Departamentos
    departments = [
        {"name": "Marketing", "code": "MKT", "manager_name": "Gerente de Marketing"},
        {"name": "Comercial", "code": "COM", "manager_name": "Gerente Comercial"},
        {"name": "Producto", "code": "PRD", "manager_name": "Gerente de Producto"},
        {"name": "Operación", "code": "OPS", "manager_name": "Gerente de Operación"},
        {"name": "Finanzas", "code": "FIN", "manager_name": "Gerente de Finanzas"},
    ]

    for dept_data in departments:
        dept = models.Department(**dept_data)
        db.add(dept)
    db.commit()

    # Agentes de Marketing
    marketing_dept = db.query(models.Department).filter_by(code="MKT").first()

    marketing_agents = [
        {
            "name": "Analista de Marketing",
            "role": "Analista",
            "department_id": marketing_dept.id,
            "status": models.AgentStatus.ONLINE,
            "system_prompt": "Analista de marketing especializado...",
            "current_activity": "Esperando tareas"
        },
        {
            "name": "Community Manager",
            "role": "Community Manager",
            "department_id": marketing_dept.id,
            "status": models.AgentStatus.ONLINE,
            "system_prompt": "Community manager creativo...",
            "current_activity": "Esperando tareas"
        },
        {
            "name": "Diseñador Gráfico",
            "role": "Diseñador",
            "department_id": marketing_dept.id,
            "status": models.AgentStatus.ONLINE,
            "system_prompt": "Diseñador gráfico especializado...",
            "current_activity": "Esperando tareas"
        },
        {
            "name": "Paid Media",
            "role": "Paid Media Specialist",
            "department_id": marketing_dept.id,
            "status": models.AgentStatus.ONLINE,
            "system_prompt": "Especialista en medios pagados...",
            "current_activity": "Esperando tareas"
        },
        {
            "name": "Reportador Marketing",
            "role": "Reportador",
            "department_id": marketing_dept.id,
            "status": models.AgentStatus.ONLINE,
            "system_prompt": "Analista de reportes...",
            "current_activity": "Esperando tareas"
        }
    ]

    for agent_data in marketing_agents:
        agent = models.Agent(**agent_data)
        db.add(agent)

    db.commit()
    logger.info("✅ Datos iniciales creados")

# ==================== ENDPOINTS ====================

@app.get("/")
async def root():
    return {
        "message": "Agentes IA - Backend API",
        "version": "1.0.0",
        "status": "online"
    }

@app.get("/api/departments")
async def get_departments(db: Session = Depends(get_db)):
    """Obtener todos los departamentos"""
    departments = db.query(models.Department).all()
    return departments

@app.get("/api/agents")
async def get_agents(db: Session = Depends(get_db)):
    """Obtener todos los agentes"""
    agents = db.query(models.Agent).all()
    return agents

@app.get("/api/agents/status")
async def get_agents_status(db: Session = Depends(get_db)):
    """Obtener estado de todos los agentes"""
    agents = db.query(models.Agent).all()
    return [{
        "id": agent.id,
        "name": agent.name,
        "role": agent.role,
        "department": agent.department.name,
        "status": agent.status.value,
        "current_activity": agent.current_activity,
        "last_active": agent.last_active.isoformat() if agent.last_active else None
    } for agent in agents]

@app.post("/api/workflows/marketing/run")
async def run_marketing_workflow(
    payload: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Ejecutar workflow de marketing"""
    try:
        logger.info("🚀 Iniciando workflow de Marketing...")

        # Crear workflow
        workflow = create_marketing_workflow()

        # Estado inicial
        initial_state = {
            "objetivo": payload.get("objetivo", "Generar contenido semanal para redes sociales"),
            "fecha_inicio": datetime.now().isoformat(),
            "analisis_competencia": "",
            "directrices_contenido": "",
            "insights_paid_media": "",
            "grilla_contenido": "",
            "copy_posts": "",
            "diseños_organicos": "",
            "campañas_creadas": "",
            "diseños_paid": "",
            "posts_publicados": "",
            "reporte": "",
            "messages": [],
            "errors": []
        }

        # Registrar ejecución
        execution = models.WorkflowExecution(
            department_id=db.query(models.Department).filter_by(code="MKT").first().id,
            workflow_name="Marketing Weekly Content",
            status=models.TaskStatus.IN_PROGRESS,
            input_data=payload,
            started_at=datetime.now()
        )
        db.add(execution)
        db.commit()

        # Broadcast inicio
        await manager.broadcast({
            "type": "workflow_started",
            "department": "Marketing",
            "execution_id": execution.id,
            "timestamp": datetime.now().isoformat()
        })

        # Ejecutar workflow
        final_state = await workflow.ainvoke(initial_state)

        # Actualizar ejecución
        execution.status = models.TaskStatus.COMPLETED
        execution.completed_at = datetime.now()
        execution.results = final_state
        db.commit()

        # Broadcast finalización
        await manager.broadcast({
            "type": "workflow_completed",
            "department": "Marketing",
            "execution_id": execution.id,
            "timestamp": datetime.now().isoformat()
        })

        logger.info("✅ Workflow de Marketing completado")

        return {
            "success": True,
            "execution_id": execution.id,
            "status": "completed",
            "results": final_state,
            "messages": final_state.get("messages", []),
            "errors": final_state.get("errors", [])
        }

    except Exception as e:
        logger.error(f"❌ Error en workflow: {str(e)}")

        if 'execution' in locals():
            execution.status = models.TaskStatus.FAILED
            execution.error_message = str(e)
            execution.completed_at = datetime.now()
            db.commit()

        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/workflows/executions")
async def get_workflow_executions(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Obtener historial de ejecuciones"""
    executions = db.query(models.WorkflowExecution)\
        .order_by(models.WorkflowExecution.started_at.desc())\
        .limit(limit)\
        .all()

    return [{
        "id": ex.id,
        "workflow_name": ex.workflow_name,
        "department": ex.department_id,
        "status": ex.status.value,
        "started_at": ex.started_at.isoformat(),
        "completed_at": ex.completed_at.isoformat() if ex.completed_at else None,
        "error": ex.error_message
    } for ex in executions]

@app.get("/api/activities")
async def get_recent_activities(
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Obtener actividades recientes"""
    activities = db.query(models.Activity)\
        .order_by(models.Activity.created_at.desc())\
        .limit(limit)\
        .all()

    return [{
        "id": act.id,
        "agent": act.agent.name,
        "department": act.agent.department.name,
        "action": act.action,
        "details": act.details,
        "timestamp": act.created_at.isoformat()
    } for act in activities]

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo back for now
            await websocket.send_text(f"Received: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=os.getenv("API_RELOAD", "True").lower() == "true"
    )
