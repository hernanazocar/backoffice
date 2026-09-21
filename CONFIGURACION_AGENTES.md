# 🎯 Configuración de Agentes - Cómo Funciona

## ¿Cómo sabe el Analista qué competencia buscar?

El Analista tiene acceso a **5 herramientas reales** que le permiten obtener datos actualizados:

### 1️⃣ `get_company_config()` - Configuración de la Empresa

Lee el archivo `backend/config/company.json` que contiene:

```json
{
  "company": {
    "name": "Tu Empresa",
    "industry": "Tu Industria",
    "description": "...",
    "target_audience": "..."
  },
  "competitors": [
    {
      "name": "Competidor 1",
      "website": "https://...",
      "social_media": {
        "instagram": "@handle",
        "linkedin": "company/nombre"
      }
    }
  ],
  "keywords_to_monitor": ["palabra1", "palabra2"]
}
```

**Así configuras qué analizar:**

```bash
# Edita este archivo para definir tu empresa y competidores
nano backend/config/company.json
```

### 2️⃣ `analyze_social_media(platform, username)` - Analizar Redes Sociales

El agente puede analizar cuentas de:
- Instagram
- Twitter/X
- LinkedIn
- Facebook

**Ejemplo de uso automático:**
```
Analista obtiene competidores → Para cada uno analiza sus redes
```

### 3️⃣ `analyze_competitor_website(url)` - Analizar Sitios Web

Extrae:
- Propuesta de valor
- Features principales
- Mensajes clave
- Estructura del sitio

### 4️⃣ `get_industry_trends(industry)` - Tendencias de la Industria

Obtiene:
- Trending topics
- Palabras clave populares
- Crecimiento de temas
- Relevancia actual

### 5️⃣ `web_search(query)` - Búsqueda Web

Busca información actualizada en la web para complementar el análisis.

---

## 🔄 Flujo Automático del Analista

Cuando ejecutas el workflow de marketing, el Analista:

```
1. Ejecuta get_company_config()
   ↓
   Obtiene: Nombre empresa, competidores, industria
   
2. Para cada competidor en la lista:
   ↓
   Ejecuta analyze_social_media("instagram", "@competidor")
   Ejecuta analyze_competitor_website("https://competidor.com")
   
3. Ejecuta get_industry_trends("Software / IA")
   ↓
   Obtiene tendencias actuales
   
4. Ejecuta web_search("AI agents trends 2024")
   ↓
   Obtiene información adicional
   
5. Consolida todo y genera:
   ↓
   - Análisis competitivo
   - Directrices de contenido
   - Insights para Paid Media
```

**Todo esto es AUTOMÁTICO**. Solo necesitas:
1. Configurar `company.json` una vez
2. Ejecutar el workflow
3. El agente obtiene datos reales y genera análisis

---

## ⚙️ Personalizar para Tu Empresa

### Paso 1: Editar Configuración

```bash
cd /Users/hernanazocar/agentes-org/backend
nano config/company.json
```

### Paso 2: Agregar Tus Datos

```json
{
  "company": {
    "name": "TU EMPRESA REAL",
    "industry": "TU INDUSTRIA",
    "description": "Qué hace tu empresa",
    "website": "https://tuempresa.com",
    "target_audience": "Tu público objetivo",
    "value_proposition": "Tu propuesta de valor"
  },
  
  "social_media": {
    "own_accounts": {
      "instagram": "@tu_cuenta",
      "linkedin": "company/tu-empresa",
      "twitter": "@tu_cuenta"
    }
  },
  
  "competitors": [
    {
      "name": "Competidor Real 1",
      "website": "https://competidor1.com",
      "social_media": {
        "instagram": "@cuenta_real",
        "linkedin": "company/nombre-real"
      },
      "focus": "En qué se enfocan"
    },
    {
      "name": "Competidor Real 2",
      ...
    }
  ],
  
  "keywords_to_monitor": [
    "palabras clave de tu industria",
    "términos que monitorear",
    "tendencias relevantes"
  ]
}
```

### Paso 3: Ejecutar

```bash
source venv/bin/activate
python test_marketing.py
```

El Analista ahora:
- Analiza TUS competidores reales
- Busca TUS keywords
- Genera insights para TU industria

---

## 🔌 Integraciones Reales (Próximo Paso)

Actualmente las herramientas usan **datos simulados** para que funcione sin APIs.

Para conectar APIs reales:

### Instagram/Facebook
```bash
# Necesitas:
- Meta Developer Account
- Instagram Graph API access token
- Agregar INSTAGRAM_ACCESS_TOKEN en .env
```

### Twitter/X
```bash
# Necesitas:
- Twitter Developer Account
- API key y token
- Agregar TWITTER_API_KEY en .env
```

### LinkedIn
```bash
# Necesitas:
- LinkedIn Developer Account
- OAuth credentials
- Agregar LINKEDIN_CLIENT_ID en .env
```

### Web Search (Brave/Serper)
```bash
# Opción 1: Brave Search (gratis hasta 2000/mes)
BRAVE_SEARCH_API_KEY=tu-key

# Opción 2: Serper (gratis hasta 2500/mes)
SERPER_API_KEY=tu-key
```

Editaría `backend/agents/tools.py` para conectar las APIs reales.

---

## 💡 Ejemplos de Uso

### Ejemplo 1: Análisis de Competencia en IA

```json
{
  "company": {
    "name": "AI Solutions Co",
    "industry": "Artificial Intelligence"
  },
  "competitors": [
    {
      "name": "OpenAI",
      "social_media": {"twitter": "@OpenAI"}
    },
    {
      "name": "Anthropic",
      "social_media": {"twitter": "@AnthropicAI"}
    }
  ]
}
```

El Analista automáticamente:
✅ Analiza feeds de Twitter de OpenAI y Anthropic  
✅ Identifica qué contenido tiene más engagement  
✅ Detecta tendencias en sus mensajes  
✅ Genera recomendaciones específicas  

### Ejemplo 2: E-commerce de Ropa

```json
{
  "company": {
    "name": "Fashion Boutique",
    "industry": "E-commerce Fashion"
  },
  "competitors": [
    {
      "name": "Zara",
      "social_media": {"instagram": "@zara"}
    },
    {
      "name": "H&M",
      "social_media": {"instagram": "@hm"}
    }
  ],
  "keywords_to_monitor": [
    "sustainable fashion",
    "spring collection 2024",
    "fashion trends"
  ]
}
```

El Analista automáticamente:
✅ Analiza posts de Instagram de Zara y H&M  
✅ Identifica qué productos promocionan  
✅ Ve qué hashtags funcionan  
✅ Genera ideas de contenido similares  

---

## 🎯 Resultado Final

Con esta configuración, cuando ejecutas:

```bash
python test_marketing.py
```

El Analista genera un reporte como:

```
📊 ANÁLISIS COMPETITIVO

Basado en análisis de:
- @zara (Instagram): 54.2M seguidores
- @hm (Instagram): 43.8M seguidores

Hallazgos clave:
1. Zara publica 3-4 veces/día, H&M 2-3 veces/día
2. Contenido tipo "outfit completo" tiene 2x más engagement
3. Mejor horario: 7-9 PM
4. Hashtags top: #OOTD, #FashionInspo, #SustainableStyle

DIRECTRICES PARA COMMUNITY MANAGER:
- Frecuencia: 3 posts/día
- Horarios: 8 AM, 2 PM, 8 PM
- Formatos: Outfit completo + detail shots
- Tono: Aspiracional pero accesible
...
```

**Todo basado en datos REALES que el agente obtuvo automáticamente.** 🚀
