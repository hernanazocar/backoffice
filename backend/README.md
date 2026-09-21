# 🤖 Sistema de Agentes IA - Backend

Sistema completo de orquestación de agentes de IA para gestión empresarial con LangGraph y Claude.

## 📋 Requisitos

- Python 3.10+
- PostgreSQL (opcional, usa SQLite por defecto)
- Redis (opcional, para producción)
- API Key de Anthropic (Claude)

## 🚀 Instalación Rápida

### 1. Instalar dependencias

```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita `.env` y agrega tu API key de Anthropic:

```env
ANTHROPIC_API_KEY=tu-api-key-aqui
```

### 3. Iniciar el servidor

```bash
python main.py
```

El servidor estará disponible en `http://localhost:8000`

## 📚 Documentación API

Una vez iniciado el servidor, accede a:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🎯 Endpoints Principales

### Agentes

- `GET /api/agents` - Listar todos los agentes
- `GET /api/agents/status` - Estado en tiempo real de agentes

### Workflows

- `POST /api/workflows/marketing/run` - Ejecutar workflow de marketing
- `GET /api/workflows/executions` - Historial de ejecuciones

### Actividades

- `GET /api/activities` - Actividades recientes del sistema

### WebSocket

- `WS /ws` - Conexión para actualizaciones en tiempo real

## 🔄 Flujo de Trabajo de Marketing

El sistema implementa el siguiente flujo automático:

```
1. Analista de Marketing
   ├─> Analiza redes sociales
   ├─> Revisa competencia
   └─> Genera directrices

2. Community Manager (Grilla)
   ├─> Crea grilla de contenido
   └─> Escribe copy

3. Diseñador Gráfico (Orgánico)
   ├─> Crea diseños para posts
   └─> Optimiza para cada red

4. Community Manager (Publicar)
   └─> Publica contenido

// EN PARALELO:

5. Paid Media
   ├─> Crea campañas pagadas
   └─> Define audiencias

6. Diseñador Gráfico (Paid)
   └─> Crea diseños para ads

7. Reportador
   └─> Genera reporte para Gerente
```

## 🧪 Probar el Sistema

### Ejecutar workflow de marketing

```bash
curl -X POST http://localhost:8000/api/workflows/marketing/run \
  -H "Content-Type: application/json" \
  -d '{
    "objetivo": "Crear contenido para lanzamiento de producto nuevo"
  }'
```

### Ver estado de agentes

```bash
curl http://localhost:8000/api/agents/status
```

## 📦 Estructura del Proyecto

```
backend/
├── main.py                 # API principal FastAPI
├── requirements.txt        # Dependencias Python
├── .env.example           # Variables de entorno
├── database/
│   ├── models.py          # Modelos SQLAlchemy
│   └── connection.py      # Configuración DB
├── agents/
│   ├── base_agent.py      # Clase base de agentes
│   └── marketing/
│       ├── team.py        # Agentes de marketing
│       └── workflow.py    # Workflow LangGraph
├── api/                   # Endpoints adicionales
├── services/              # Lógica de negocio
└── utils/                 # Utilidades
```

## 🔐 Seguridad

- Nunca commitees el archivo `.env`
- Guarda tu API key de Anthropic de forma segura
- En producción, usa PostgreSQL + Redis
- Implementa autenticación JWT para endpoints

## 🐛 Debugging

Ver logs en tiempo real:

```bash
tail -f logs/app.log
```

## 📈 Próximos Pasos

1. ✅ Sistema base funcionando
2. ⏳ Integrar con APIs de redes sociales (Meta, Twitter, LinkedIn)
3. ⏳ Conectar frontend con WebSockets
4. ⏳ Implementar workflows para otros departamentos
5. ⏳ Sistema de caché con Redis
6. ⏳ Métricas y monitoreo con Prometheus

## 🆘 Soporte

Si encuentras problemas:
1. Verifica que tu API key de Anthropic sea válida
2. Revisa los logs en consola
3. Asegúrate de tener todas las dependencias instaladas
