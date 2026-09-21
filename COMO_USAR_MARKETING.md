# 🚀 Cómo Usar el Sistema de Marketing Automatizado

Sistema completo de Marketing con agentes IA que generan contenido, diseñan piezas y publican en redes sociales.

---

## 📋 RESUMEN DEL SISTEMA

### Lo que hace AUTOMÁTICAMENTE:
1. **Community Manager** → Genera copies para posts
2. **Diseñador Gráfico** → Crea diseños con DALL-E
3. **Sistema de Aprobación** → Te muestra todo listo para aprobar
4. **Publicación Automática** → Publica en Instagram/Facebook/LinkedIn

### Tu trabajo:
- ✅ Revisar el contenido generado
- ✅ Click "Aprobar" o "Rechazar"  
- ✅ Eso es todo!

---

## 🔧 INSTALACIÓN (Primera vez)

### 1. Instalar dependencias

```bash
cd /Users/hernanazocar/developers/agentes-org/backend

# Activar entorno virtual
source venv/bin/activate

# Instalar requirements
pip install -r requirements-marketing.txt
```

### 2. Configurar credenciales (.env)

Edita el archivo `.env`:

```bash
# OpenAI (para DALL-E - generar diseños)
OPENAI_API_KEY=sk-...

# Meta/Facebook (para Instagram y Facebook)
META_ACCESS_TOKEN=tu_token
META_PAGE_ID=tu_page_id

# LinkedIn (opcional)
LINKEDIN_ACCESS_TOKEN=tu_token
LINKEDIN_ORG_ID=tu_org_id
```

**¿No tienes las credenciales aún?**
- No problem! El sistema funciona en **modo MOCK** sin ellas
- Genera todo el contenido pero simula la publicación
- Perfecto para testing

---

## 🚀 USAR EL SISTEMA

### Opción A: Modo RÁPIDO (Todo automático)

```bash
cd /Users/hernanazocar/developers/agentes-org/backend

# Iniciar la API
./start_marketing_api.sh
```

Esto inicia:
- ✅ API REST en `http://localhost:5000`
- ✅ Endpoints para aprobar/rechazar posts
- ✅ Sistema de generación de diseños
- ✅ Integración con redes sociales

### Opción B: Paso a Paso

```bash
# Terminal 1: Iniciar API
cd backend
python3 api/marketing_api.py

# Terminal 2: Iniciar Dashboard
cd dashboard  
python3 -m http.server 8000

# Abrir en navegador
open http://localhost:8000
```

---

## 📱 FLUJO COMPLETO DE USO

### 1. Los agentes generan contenido (automático - 6AM)

```
Community Manager:
└── Genera 7 posts para la semana
    └── Cada post tiene: copy, hashtags, horario, plataforma
    └── Se guardan en: /posts/pending/

Diseñador Gráfico:
└── Lee los posts pendientes
    └── Genera diseño con DALL-E para cada uno
    └── Vincula la imagen al post
```

### 2. Tú revisas en el Dashboard

```
Dashboard muestra:
📋 7 posts pendientes de aprobación

Cada post muestra:
- 📝 Copy completo
- 🎨 Diseño generado (preview)
- 📱 Plataforma (Instagram/Facebook)
- 🕐 Horario programado
- #️⃣ Hashtags
```

### 3. Apruebas con 1 click

```
Click en "✅ Aprobar y Publicar"

El sistema automáticamente:
1. Verifica que tenga diseño ✓
2. Publica en Instagram ✓  
3. Publica en Facebook ✓
4. Programa para el horario indicado ✓
5. Guarda registro de publicación ✓
```

---

## 🧪 PROBAR EL SISTEMA (Mock Mode)

### Crear un post de prueba

```bash
cd backend
python3 approval_system/post_manager.py
```

Esto:
1. Crea un post de ejemplo
2. Genera diseño mock
3. Lo aprueba
4. Simula publicación
5. Muestra resultados

**Output esperado:**
```
✓ Post creado: post_20260921_140530
✓ Diseño generado: https://placeholder.com/mock-design.png
[MOCK] Publicando en Instagram:
  Copy: 🚀 ¿Sabías que el 80%...
  Imagen: https://placeholder.com/mock-design.png
  Programado: 2026-09-22 19:00
✓ Publicado en instagram: mock_ig_1726936830.0
✓ Post aprobado y publicado exitosamente!
```

---

## 🌐 API ENDPOINTS

### GET /api/marketing/posts/pending
Obtiene posts pendientes de aprobación

```bash
curl http://localhost:5000/api/marketing/posts/pending
```

### POST /api/marketing/posts/{id}/approve
Aprueba y publica un post

```bash
curl -X POST http://localhost:5000/api/marketing/posts/post_123/approve
```

### POST /api/marketing/posts/{id}/reject
Rechaza un post

```bash
curl -X POST http://localhost:5000/api/marketing/posts/post_123/reject \
  -H "Content-Type: application/json" \
  -d '{"reason": "Copy necesita mejoras"}'
```

### PUT /api/marketing/posts/{id}/edit
Edita un post antes de aprobar

```bash
curl -X PUT http://localhost:5000/api/marketing/posts/post_123/edit \
  -H "Content-Type: application/json" \
  -d '{"copy": "Nuevo copy mejorado..."}'
```

---

## 🎨 CÓMO FUNCIONA LA GENERACIÓN DE DISEÑOS

### Community Manager crea el post:

```json
{
  "copy": "🚀 ¿Sabías que el 80%...",
  "platforms": ["instagram"],
  "needs_design": true,
  "design_spec": {
    "concept": "Gradiente moderno con icono",
    "colors": ["#FF6B35", "#EC4899"],
    "style": "modern minimalist",
    "layout": "centered"
  }
}
```

### Diseñador Gráfico genera con DALL-E:

```
Prompt enviado a DALL-E:
"Create a professional social media post design for Instagram.
 Concept: Gradiente moderno con icono
 Style: modern minimalist
 Colors: gradient from #FF6B35 to #EC4899
 Layout: centered composition
 ..."

↓

DALL-E genera imagen HD (1024x1024)
↓
Se descarga y guarda en: /assets/marketing/2026-09-21/post_123.png
↓
Se vincula al post
```

---

## 📊 VER ANALÍTICAS DE POSTS

Una vez publicado, puedes ver métricas:

```bash
curl http://localhost:5000/api/marketing/posts/post_123/analytics
```

Retorna:
```json
{
  "success": true,
  "analytics": {
    "instagram": {
      "likes": 342,
      "comments": 28,
      "reach": 1847,
      "impressions": 2103,
      "engagement_rate": 3.8
    }
  }
}
```

---

## 🔀 CAMBIAR DE MOCK A PRODUCCIÓN

### Modo MOCK (Default)
- No requiere credenciales API
- Simula todo
- Perfecto para testing
- Genera archivos placeholder

### Modo PRODUCCIÓN

```python
# En: backend/api/marketing_api.py

# Cambiar esta línea:
post_manager = PostManager(mock_mode=False)  # False = real APIs
```

Requisitos para producción:
1. ✅ Configurar `.env` con tokens reales
2. ✅ Tener credenciales de Meta API
3. ✅ Tener API key de OpenAI
4. ✅ Configurar LinkedIn/Twitter (opcional)

---

## 🛠️ SOLUCIÓN DE PROBLEMAS

### Error: "OpenAI API key not configured"
→ Agregar `OPENAI_API_KEY` al `.env`

### Error: "Meta credentials not configured"
→ Agregar `META_ACCESS_TOKEN` y `META_PAGE_ID` al `.env`

### Los posts no aparecen en pending
→ Los agentes aún no han corrido. Ejecuta manualmente:
```bash
python3 backend/ejecutar_workflow.py marketing
```

### No genera imágenes
→ Verifica que tengas créditos en OpenAI y la API key correcta

---

## 📁 ESTRUCTURA DE ARCHIVOS

```
backend/
├── integrations/
│   ├── social_media.py      # Publicación en redes
│   └── design_ai.py          # Generación de diseños
├── approval_system/
│   └── post_manager.py       # Gestión de posts
├── api/
│   └── marketing_api.py      # API REST
├── prompts/marketing/        # Prompts de agentes
├── .env                      # Credenciales (no subir a git)
└── start_marketing_api.sh    # Script de inicio

posts/
├── pending/                  # Posts por aprobar
├── approved/                 # Posts aprobados
├── published/                # Posts publicados
└── rejected/                 # Posts rechazados

assets/marketing/
└── 2026-09-21/              # Imágenes por fecha
    ├── post_123.png
    └── post_124.png
```

---

## ✅ PRÓXIMOS PASOS

1. **Probar en modo mock**:
   ```bash
   ./backend/start_marketing_api.sh
   ```

2. **Crear contenido de prueba**:
   ```bash
   python3 backend/approval_system/post_manager.py
   ```

3. **Revisar en el dashboard**:
   ```
   http://localhost:8000
   ```

4. **Cuando esté listo, configurar APIs reales**

5. **Activar agentes automáticos** (cron jobs en cloud)

---

## 💡 TIPS

- **Revisa los diseños** antes de publicar - DALL-E a veces se equivoca con texto
- **Edita los copies** si algo no te gusta - no estás obligado a aceptar todo
- **Programa los posts** para horarios óptimos (7-9 PM mejor engagement)
- **Monitorea analíticas** para ver qué contenido funciona mejor

---

**¡El sistema está listo para usar!** 🚀

¿Dudas? Revisa los logs en:
- Backend: Terminal donde corre la API
- Posts: `backend/posts/`
- Imágenes: `backend/assets/marketing/`
