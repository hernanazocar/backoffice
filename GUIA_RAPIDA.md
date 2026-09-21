# 🚀 Guía Rápida - Ejecutar Workflows

## ⚡ Inicio Rápido (3 pasos)

### 1️⃣ Iniciar el Backend

```bash
cd /Users/hernanazocar/agentes-org/backend
source venv/bin/activate
python main.py
```

Deja esta terminal abierta. El servidor corre en `http://localhost:8000`

### 2️⃣ Ejecutar Workflow (nueva terminal)

```bash
cd /Users/hernanazocar/agentes-org/backend
source venv/bin/activate
python ejecutar_workflow.py
```

### 3️⃣ Elegir Qué Hacer

```
🤖 SISTEMA DE AGENTES IA - EJECUTAR WORKFLOWS

Selecciona qué workflow ejecutar:

1. Análisis básico de competencia
2. Comparar precios por zona
3. Identificar influencers tech
4. Salir

Elige opción (1-4): _
```

---

## 📝 Dónde y Cómo Dar Instrucciones

### Opción A: Usar el Script Interactivo (RECOMENDADO)

```bash
python ejecutar_workflow.py
```

- Elige la opción del menú
- El script ya tiene ejemplos configurados
- Ve cómo funcionan las instrucciones

### Opción B: Editar el Script para Tu Caso

Abre `ejecutar_workflow.py` y modifica:

```python
async def mi_analisis_personalizado():
    payload = {
        "objetivo": "TU OBJETIVO AQUÍ",
        
        "instrucciones_analista": {
            "tarea_especial": "lo_que_necesites",
            "parametros": "tus parámetros",
            # Agrega lo que necesites
        }
    }
    
    # Ejecutar
    async with httpx.AsyncClient(timeout=300.0) as client:
        response = await client.post(
            "http://localhost:8000/api/workflows/marketing/run",
            json=payload
        )
        print(response.json())
```

### Opción C: Llamada directa con cURL

```bash
curl -X POST http://localhost:8000/api/workflows/marketing/run \
  -H "Content-Type: application/json" \
  -d '{
    "objetivo": "Evaluar precios en Zona Norte",
    "instrucciones_analista": {
      "zona": "Zona Norte Santiago",
      "competidores": ["Líder", "Jumbo"],
      "productos": ["Leche", "Pan"]
    }
  }'
```

### Opción D: Desde el Navegador (Swagger UI)

1. Abre: http://localhost:8000/docs
2. Expande: `POST /api/workflows/marketing/run`
3. Click: "Try it out"
4. Pega el JSON:

```json
{
  "objetivo": "Tu objetivo aquí",
  "instrucciones_analista": {
    "lo_que_necesites": "tus parámetros"
  }
}
```

5. Click: "Execute"

---

## 📊 Ejemplos Reales

### Ejemplo 1: Análisis de Precios

```python
payload = {
    "objetivo": "Comparar precios supermercados Zona Norte",
    "instrucciones_analista": {
        "zona": "Zona Norte, Santiago",
        "competidores": ["Líder", "Jumbo", "Unimarc"],
        "productos": ["Leche 1L", "Pan", "Arroz 1kg"],
        "que_buscar": "Precio actual en cada tienda"
    }
}
```

### Ejemplo 2: Analizar Influencers

```python
payload = {
    "objetivo": "Encontrar influencers tech para colaborar",
    "instrucciones_analista": {
        "plataforma": "Twitter",
        "region": "LATAM",
        "followers_min": 10000,
        "temas": ["IA", "Startups", "Tech"]
    }
}
```

### Ejemplo 3: Sentimiento de Marca

```python
payload = {
    "objetivo": "Medir sentimiento sobre nuestra marca",
    "instrucciones_analista": {
        "marca": "Nombre de tu empresa",
        "periodo": "últimos 30 días",
        "fuentes": ["Twitter", "Instagram", "LinkedIn"],
        "que_analizar": ["Positivo/Negativo", "Temas recurrentes"]
    }
}
```

---

## 🎯 Cómo Funciona

```
TÚ escribes instrucciones en JSON
         ↓
Se envían al backend (/api/workflows/marketing/run)
         ↓
Agente Analista las recibe
         ↓
Agente usa sus HERRAMIENTAS para obtener datos
         ↓
Agente genera análisis basado en datos reales
         ↓
Recibes el resultado
```

---

## ⚙️ Configuración Permanente vs Temporal

### Configuración Permanente (company.json)

Para competidores que SIEMPRE analizas:

```bash
nano backend/config/company.json
```

### Instrucciones Temporales (ejecutar_workflow.py)

Para análisis ESPECÍFICOS de una sola vez.

**No necesitas editar company.json cada vez.**

---

## 🐛 Solución de Problemas

### Error: "Connection refused"

```bash
# El backend no está corriendo
# Solución:
cd backend
python main.py
```

### Error: "Invalid API key"

```bash
# Tu API key de Anthropic no está configurada
# Solución:
nano backend/.env
# Agrega: ANTHROPIC_API_KEY=tu-key-real
```

### El workflow tarda mucho

Es normal. Cada agente toma 10-30 segundos. El workflow completo: 2-5 minutos.

---

## 📚 Más Información

- **Cómo funciona:** `COMO_FUNCIONA_REALMENTE.md`
- **Configurar agentes:** `CONFIGURACION_AGENTES.md`
- **Setup completo:** `SETUP_COMPLETO.md`

---

## ✅ Resumen

```bash
# Terminal 1: Iniciar backend
cd backend && python main.py

# Terminal 2: Ejecutar workflow
cd backend && python ejecutar_workflow.py

# Elige opción del menú
# ¡Listo!
```

**Así de simple.** 🚀
