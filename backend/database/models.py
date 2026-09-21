from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, JSON, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class AgentStatus(str, enum.Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    WORKING = "working"
    ERROR = "error"

class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(10), unique=True, nullable=False)
    description = Column(Text)
    manager_name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    agents = relationship("Agent", back_populates="department")
    tasks = relationship("Task", back_populates="department")

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    status = Column(Enum(AgentStatus), default=AgentStatus.OFFLINE)
    system_prompt = Column(Text, nullable=False)
    current_activity = Column(String(200))
    config = Column(JSON)  # Configuración específica del agente
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)

    department = relationship("Department", back_populates="agents")
    tasks = relationship("Task", back_populates="agent")
    activities = relationship("Activity", back_populates="agent")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    department_id = Column(Integer, ForeignKey("departments.id"))
    agent_id = Column(Integer, ForeignKey("agents.id"))
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    priority = Column(Integer, default=0)
    dependencies = Column(JSON)  # IDs de tareas de las que depende
    input_data = Column(JSON)  # Datos de entrada
    result = Column(JSON)  # Resultado de la ejecución
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)

    department = relationship("Department", back_populates="tasks")
    agent = relationship("Agent", back_populates="tasks")
    activities = relationship("Activity", back_populates="task")

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"))
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    action = Column(String(200), nullable=False)
    details = Column(Text)
    extra_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    agent = relationship("Agent", back_populates="activities")
    task = relationship("Task", back_populates="activities")

class WorkflowExecution(Base):
    __tablename__ = "workflow_executions"

    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"))
    workflow_name = Column(String(100), nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    input_data = Column(JSON)
    results = Column(JSON)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    error_message = Column(Text)
