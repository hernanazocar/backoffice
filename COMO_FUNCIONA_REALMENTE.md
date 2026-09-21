# 🎯 Cómo Funciona el Sistema REALMENTE

## Tu Pregunta
> "¿Cómo el agente Analista sabrá dónde buscar, qué competencia analizar? ¿Qué pasa si un día necesito que evalúe precios en una zona particular?"

---

## 📊 **Arquitectura Actual (3 Niveles)**

### **Nivel 1: Configuración Base (company.json)**

```
backend/config/company.json
```

**Qué contiene:**
- Tu empresa (nombre, industria, propuesta)
- Competidores fijos (nombres, redes, websites)
- Keywords estándar

**Cuándo se usa:**
- Para análisis RUTINARIOS
- Cuando ejecutas sin instrucciones específicas
- Es el "conocimiento base" del agente

**Ejemplo:**
```json
{
  "competitors": [
    {"name": "Competidor A", "instagram": "@competidorA"},
    {"name": "Competidor B", "website": "https://..."}
  ]
}
```

El agente lee esto y sabe: "Estos son los competidores que siempre debo analizar"

---

### **Nivel 2: Instrucciones Dinámicas por Ejecución**

**Cuando ejecutas el workflow, puedes darle instrucciones ESPECÍFICAS:**

```python
# Análisis Normal (usa company.json)
payload = {
    "objetivo": "Contenido semanal para redes"
}

# Análisis ESPECÍFICO (ignora company.json, usa estas instrucciones)
payload = {
    "objetivo": "Evaluar precios en Zona Norte",
    "instrucciones_analista": {
        "tarea": "evaluar_precios",
        "zona": "Zona Norte, Santiago",
        "competidores": ["Líder", "Jumbo", "Unimarc"],
        "productos": ["Leche 1L", "Pan", "Arroz 1kg"],
        "que_hacer": "Busca precios actuales en web de estos productos"
    }
}
```

**El agente recibe esto y:**
1. Lee las instrucciones específicas
2. Usa las herramientas para buscar lo que le pediste
3. Ignora (o complementa) company.json

---

### **Nivel 3: Herramientas Extensibles**

El agente tiene 5 herramientas **YA IMPLEMENTADAS**:

| Herramienta | Para Qué Sirve | Ejemplo de Uso |
|-------------|----------------|----------------|
| `get_company_config()` | Leer company.json | Análisis rutinario |
| `web_search(query)` | Buscar en web | "Precios Jumbo zona norte" |
| `analyze_social_media(platform, user)` | Analizar redes | Instagram de @competidor |
| `analyze_competitor_website(url)` | Analizar sitios | https://competidor.com |
| `get_industry_trends(industry)` | Tendencias | "E-commerce Chile" |

**Si mañana necesitas algo nuevo**, agregas una herramienta:

```python
# En backend/agents/tools.py

async def analyze_prices_by_zone(zone: str, competitors: List[str]) -> Dict:
    """Nueva herramienta para analizar precios por zona"""
    # Tu lógica aquí
    return {"precios": [...]}
```

Y el agente puede usarla automáticamente.

---

## 🔄 **Flujo Completo: Ejemplo Real**

### **Caso 1: Análisis Rutinario de Competencia**

```bash
# Tú ejecutas:
curl -X POST http://localhost:8000/api/workflows/marketing/run \
  -d '{"objetivo": "Contenido semanal"}'
```

**Lo que pasa:**

```
1. Agente Analista inicia
   ↓
2. Ejecuta get_company_config()
   → Obtiene: ["Competidor A", "Competidor B", "Competidor C"]
   ↓
3. Para cada competidor:
   - Ejecuta analyze_social_media("instagram", "@competidorA")
   - Ejecuta analyze_competitor_website("https://competidorA.com")
   ↓
4. Ejecuta get_industry_trends("tu_industria")
   ↓
5. Consolida TODO y genera:
   - Análisis competitivo
   - Directrices de contenido
   - Insights para Paid Media
```

---

### **Caso 2: Análisis Específico (Precios en Zona)**

```bash
# Tú ejecutas:
curl -X POST http://localhost:8000/api/workflows/marketing/run \
  -d '{
    "objetivo": "Evaluar precios zona norte",
    "instrucciones_analista": {
      "zona": "Zona Norte Santiago",
      "competidores": ["Líder", "Jumbo"],
      "productos": ["Leche", "Pan", "Arroz"]
    }
  }'
```

**Lo que pasa:**

```
1. Agente Analista recibe instrucciones ESPECÍFICAS
   ↓
2. Lee: "Debo evaluar precios de Líder y Jumbo en Zona Norte"
   ↓
3. Ejecuta web_search("precios Líder zona norte Santiago")
   ↓
4. Ejecuta web_search("precios Jumbo zona norte Santiago")
   ↓
5. Para cada producto:
   - Busca precio actual
   - Compara entre tiendas
   ↓
6. Genera reporte de precios comparativo
```

---

## 💡 **Respuesta Directa a Tu Pregunta**

### ¿Cómo sabe el agente dónde buscar?

**Opción A (Rutinario):**
Lee `company.json` → Tiene lista de competidores fija

**Opción B (Específico):**
Tú le das instrucciones al ejecutar → Él busca lo que le pides

### ¿Qué pasa si un día necesito evaluar precios en zona X?

**Solución 1: Instrucciones Dinámicas (RECOMENDADO)**

```python
# test_precios_zona.py
import httpx

async def analizar_precios_zona_norte():
    payload = {
        "objetivo": "Comparar precios en Zona Norte",
        "instrucciones_analista": {
            "tarea_especial": "evaluar_precios",
            "zona_geografica": "Zona Norte, Santiago",
            "competidores": [
                "Líder (Av. Independencia 2000)",
                "Jumbo (Mall Plaza Norte)",
                "Unimarc (Huechuraba)"
            ],
            "productos_comparar": [
                {"nombre": "Leche Colun 1L", "categoria": "Lácteos"},
                {"nombre": "Pan Ideal", "categoria": "Panadería"},
                {"nombre": "Arroz Grado 1 1kg", "categoria": "Abarrotes"}
            ],
            "que_buscar": [
                "Precio actual de cada producto",
                "Promociones vigentes",
                "Disponibilidad en tienda"
            ],
            "como_buscar": "Usa web_search para buscar en sitios web de cada tienda"
        }
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/workflows/marketing/run",
            json=payload
        )
        print(response.json())
```

**El agente:**
1. Lee tus instrucciones
2. Usa `web_search("precio Leche Colun Líder Independencia")`
3. Usa `web_search("precio Leche Colun Jumbo Plaza Norte")`
4. Compara resultados
5. Genera tabla comparativa de precios

**Solución 2: Agregar Herramienta Específica**

Si vas a hacer esto SEGUIDO, creas una herramienta:

```python
# En backend/agents/tools.py

async def compare_prices_by_zone(
    zone: str,
    stores: List[str],
    products: List[str]
) -> Dict:
    """Compara precios de productos en tiendas de una zona"""
    results = []
    
    for store in stores:
        for product in products:
            # Buscar precio real (API o scraping)
            price = await get_price(store, product, zone)
            results.append({
                "store": store,
                "product": product,
                "price": price,
                "zone": zone
            })
    
    return {
        "comparison_table": results,
        "cheapest_by_product": analyze_cheapest(results),
        "average_prices": calculate_averages(results)
    }
```

Y el agente puede usarla:
```python
analista.execute_tool("compare_prices_by_zone", {
    "zone": "Zona Norte",
    "stores": ["Líder", "Jumbo"],
    "products": ["Leche", "Pan"]
})
```

---

## 🎯 **Resumen: Sistema COMPLETO**

```
┌─────────────────────────────────────────────┐
│  1. CONFIGURACIÓN BASE (company.json)       │
│     - Competidores fijos                    │
│     - Keywords estándar                     │
│     - Para análisis rutinarios              │
└─────────────────────────────────────────────┘
                    +
┌─────────────────────────────────────────────┐
│  2. INSTRUCCIONES DINÁMICAS (por ejecución) │
│     - Tareas específicas                    │
│     - Parámetros únicos                     │
│     - Sobrescribe config base               │
└─────────────────────────────────────────────┘
                    +
┌─────────────────────────────────────────────┐
│  3. HERRAMIENTAS EXTENSIBLES                │
│     - 5 herramientas base                   │
│     - Fácil agregar nuevas                  │
│     - Claude decide cuándo usarlas          │
└─────────────────────────────────────────────┘
                    =
         SISTEMA 100% FLEXIBLE
```

---

## ✅ **Para Tu Caso Específico**

### Hoy: "Analiza competidores"
```bash
python test_marketing.py
# Usa company.json con competidores fijos
```

### Mañana: "Evalúa precios en Zona Norte"
```bash
python test_precios_zona.py
# Pasa instrucciones específicas, el agente las ejecuta
```

### Pasado: "Analiza sentimiento en Twitter"
```bash
python test_sentimiento_twitter.py
# Otra tarea diferente, mismo sistema
```

**NO necesitas cambiar código. Solo pasas diferentes instrucciones.** 🚀

---

## 📝 **Archivos Clave para Entender**

1. `backend/config/company.json` → Configuración base
2. `backend/agents/tools.py` → Herramientas disponibles  
3. `backend/examples/workflows_dinamicos.py` → Ejemplos de uso
4. `backend/agents/base_agent.py` → Cómo usa herramientas

**Todo está listo. Solo necesitas ejecutar y ver cómo funciona.** ✅
