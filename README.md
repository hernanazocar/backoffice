# 🏢 BackOffice - Sistema de Agentes IA Automatizados

Sistema de gestión organizacional automatizado con agentes Claude Code que funcionan 24/7 en la nube.

## 📊 Estructura Organizacional (Universal)

### 👔 Gerencia General
- **Gerente General**: Reporte consolidado a las 8:00 AM
- **Email + Google Calendar**

### 💼 Comercial (5 agentes)
**Gerente Comercial** (Líder del área)
- Ejecutivo de Ventas
- Prospector de Leads
- Analista Comercial
- Coordinador de Cuentas

### 📢 Marketing (5 agentes)
**Gerente de Marketing** (Líder del área)
- Community Manager
- Diseñador Gráfico
- Paid Media Specialist
- Analista de Marketing

### 💰 Finanzas (5 agentes)
**Gerente de Finanzas** (Líder del área)
- Contador
- Analista Financiero
- Coordinador de Cobranzas
- Tesorero

### ⚙️ Operaciones (5 agentes)
**Gerente de Operaciones** (Líder del área)
- Coordinador Logístico
- Analista de Inventario
- Coordinador de Compras
- Asistente Administrativo

### 🤝 Atención al Cliente (5 agentes)
**Gerente de Atención al Cliente** (Líder del área)
- Ejecutivo de Soporte
- Coordinador de Reclamos
- Analista de Satisfacción
- Coordinador Postventa

## 🔄 Flujo de Trabajo Automático

### 6:00 AM - Agentes Especializados
Los 20 agentes ejecutan sus tareas específicas y generan reportes en:
```
/reportes/{departamento}/{cargo}/YYYY-MM-DD.md
Ejemplo: /reportes/marketing/community-manager/2026-09-21.md
```

### 7:00 AM - Gerentes de Área
Los 5 gerentes consolidan reportes de su departamento en:
```
/reportes/gerentes/{departamento}/YYYY-MM-DD.md
Ejemplo: /reportes/gerentes/marketing/2026-09-21.md
```

### 8:00 AM - Gerencia General
Reporte final consolidado enviado por email y calendario:
```
/reportes/gerencia-general/YYYY-MM-DD.md
```

## ✨ Tareas Puntuales

Además del flujo automático, se pueden asignar tareas específicas mediante:

### Via Dashboard
1. Abrir dashboard de monitoreo
2. Tab "Asignar Tareas"
3. Seleccionar departamento, agente y prioridad
4. El agente ejecuta la tarea en su próxima corrida

### Via Archivo JSON
Crear archivo en:
```
/tareas/{departamento}/{agente}/pendientes/{tarea-id}.json
```

Formato:
```json
{
  "id": "unique-id",
  "tipo": "puntual",
  "prioridad": "urgente|alta|normal",
  "descripcion": "Analizar competencia X en zona Y",
  "asignado_por": "gerente-{departamento}",
  "fecha_asignacion": "2026-09-14T20:00:00Z",
  "estado": "pendiente"
}
```

El agente mueve el archivo a `/completadas/` al terminar.

## 📁 Estructura del Repositorio

```
agentes-org/
├── tareas/                    # Sistema de tareas
│   ├── comercial/
│   │   ├── ejecutivo-ventas/
│   │   │   ├── pendientes/   # Tareas por ejecutar
│   │   │   └── completadas/  # Tareas finalizadas
│   │   ├── prospector-leads/
│   │   ├── analista-comercial/
│   │   └── coordinador-cuentas/
│   ├── marketing/
│   │   ├── community-manager/
│   │   ├── disenador-grafico/
│   │   ├── paid-media/
│   │   └── analista-marketing/
│   ├── finanzas/
│   ├── operaciones/
│   └── atencion-cliente/
├── reportes/                  # Reportes generados
│   ├── comercial/
│   ├── marketing/
│   ├── finanzas/
│   ├── operaciones/
│   ├── atencion-cliente/
│   ├── gerentes/             # Reportes consolidados por gerente
│   └── gerencia-general/     # Reporte final diario
└── dashboard/                # Estado en tiempo real
    └── estado-agentes.json   # Estado actual de cada agente
```

## 🎯 Dashboard de Monitoreo

URL: https://claude.ai/artifact/6nn1UToZSNW1gaRVoR7uzk

Funciones:
- ✅ Ver organigrama completo en tiempo real
- ✅ Asignar tareas puntuales a cualquier agente
- ✅ Monitorear actividad y estado de agentes
- ✅ Ver reportes recientes por departamento
- ✅ Métricas consolidadas

## ⚙️ Configuración de Agentes

Cada agente cloud está configurado con:
- **Schedule**: Cron expression en UTC
- **Repository**: Este repositorio (agentes-org)
- **MCP Connectors**: Gmail + Google Calendar
- **Environment**: Anthropic Cloud
- **Model**: Claude Sonnet 5

## 📝 Próximos Pasos

1. ✅ Crear repositorio y estructura
2. ⏳ Crear agentes cloud (26 total: 1 Gerencia General + 5 Gerentes de Área + 20 Agentes Especializados)
3. ⏳ Configurar schedules automáticos
4. ⏳ Probar flujo completo

## 🌍 Sistema Universal

Esta estructura funciona para **CUALQUIER** industria:
- ✅ Ferretería → inventario, ventas, atención
- ✅ Restaurante → reservas, delivery, postventa
- ✅ E-commerce → productos, campañas, logística
- ✅ Consultora → propuestas, proyectos, satisfacción
- ✅ Software → ventas, soporte técnico, métricas
- ✅ Y más...

---

**Creado**: 2026-09-14  
**Owner**: hernanazocar  
**Repo**: https://github.com/hernanazocar/agentes-org
