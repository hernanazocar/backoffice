# 🔑 Cómo Obtener las API Keys

## 1️⃣ ANTHROPIC (Claude) - REQUERIDO ✅

**¿Para qué?** Los agentes IA (Community Manager, Diseñador, etc.)

**Pasos:**
1. Ve a: https://console.anthropic.com/
2. Crea una cuenta o inicia sesión
3. Ve a **"API Keys"** en el menú
4. Click en **"Create Key"**
5. Copia la key (empieza con `sk-ant-...`)
6. Pégala en `.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-tu-key-aqui
   ```

**Costo:** ~$3 USD por cada 1M tokens (muy económico)

---

## 2️⃣ OPENAI (DALL-E 3) - REQUERIDO ✅

**¿Para qué?** Generar diseños automáticamente

**Pasos:**
1. Ve a: https://platform.openai.com/
2. Crea una cuenta o inicia sesión
3. Ve a **"API Keys"**
4. Click en **"Create new secret key"**
5. Copia la key (empieza con `sk-...`)
6. Pégala en `.env`:
   ```
   OPENAI_API_KEY=sk-tu-key-aqui
   ```

**Costo:** ~$0.040 por imagen (1024x1024, calidad HD)
- 7 posts semanales = $0.28/semana = ~$1.12/mes

---

## 3️⃣ META (Instagram/Facebook) - OPCIONAL ⚠️

**¿Para qué?** Publicar automáticamente en Instagram y Facebook

**Pasos:**

### A. Crear App de Facebook
1. Ve a: https://developers.facebook.com/apps
2. Click **"Create App"**
3. Tipo: **"Business"**
4. Nombre: "Backoffice Marketing Bot"

### B. Obtener Token de Página
1. En tu App, ve a **"Tools" → "Graph API Explorer"**
2. Selecciona tu página de Facebook/Instagram
3. Permisos necesarios:
   - `pages_manage_posts`
   - `pages_read_engagement`
   - `instagram_basic`
   - `instagram_content_publish`
4. Click **"Generate Access Token"**
5. Copia el token (empieza con `EAA...`)

### C. Obtener Page ID
1. Ve a tu página de Facebook
2. En la URL: `facebook.com/PAGE_NAME`
3. O usa Graph API Explorer: `me/accounts`

### D. Configura en `.env`:
```
META_ACCESS_TOKEN=EAAtu-token-aqui
META_PAGE_ID=123456789
```

**Costo:** GRATIS (con límites de API)

**⚠️ IMPORTANTE:** Si no configuras Meta, el sistema funciona igual pero **NO publica** (Mock Mode)

---

## 4️⃣ LINKEDIN - OPCIONAL ⚠️

**¿Para qué?** Publicar en LinkedIn

**Pasos:**
1. Ve a: https://www.linkedin.com/developers/apps
2. Crea una App
3. Solicita acceso a **"Share on LinkedIn"**
4. Genera token OAuth 2.0
5. Configura en `.env`:
   ```
   LINKEDIN_ACCESS_TOKEN=AQVtu-token
   LINKEDIN_ORG_ID=123456
   ```

**Costo:** GRATIS

---

## 🎯 ¿QUÉ NECESITO MÍNIMO PARA EMPEZAR?

### Opción 1: PRUEBA COMPLETA (Recomendado)
- ✅ Anthropic (Claude) - **REQUERIDO**
- ✅ OpenAI (DALL-E) - **REQUERIDO**
- ⚠️ Meta - Opcional (usa Mock Mode sin esto)
- ⚠️ LinkedIn - Opcional

**Costo mensual:** ~$10-15 USD

### Opción 2: SOLO TESTING (Sin publicar)
- ✅ Anthropic (Claude) - **REQUERIDO**
- ❌ OpenAI - Omitir (no genera imágenes reales)
- ❌ Meta - Omitir (Mock Mode)
- ❌ LinkedIn - Omitir

**Costo mensual:** ~$3-5 USD

---

## 📝 RESUMEN DE COSTOS

| Servicio | Costo Aproximado | ¿Obligatorio? |
|----------|------------------|---------------|
| Anthropic (Claude) | $3-5/mes | ✅ SÍ |
| OpenAI (DALL-E) | $1-2/mes | ✅ SÍ |
| Meta (Facebook/IG) | Gratis | ⚠️ Opcional |
| LinkedIn | Gratis | ⚠️ Opcional |
| **TOTAL** | **$4-7/mes** | - |

---

## 🚀 SIGUIENTE PASO

Después de obtener las keys:

```bash
# 1. Edita el archivo .env
nano ~/developers/backoffice/backend/.env

# 2. Pega tus keys donde dice "your-xxx-key-here"

# 3. Guarda (Ctrl+O, Enter, Ctrl+X)

# 4. Ejecuta el equipo de Marketing
cd ~/developers/backoffice/backend
python3 ejecutar_workflow.py marketing
```

---

## ❓ ¿DUDAS?

**P: ¿Puedo probar sin pagar nada?**
R: Sí, ambas APIs tienen créditos gratis iniciales (~$5 en OpenAI, $5 en Anthropic)

**P: ¿Necesito tarjeta de crédito?**
R: Sí, para verificar la cuenta (pero no te cobran hasta que uses tus créditos gratis)

**P: ¿Puedo usar el sistema sin las keys?**
R: Parcialmente. Sin Anthropic NO funciona. Sin OpenAI funciona pero sin imágenes.

**P: ¿Qué pasa si se acaban mis créditos?**
R: El sistema deja de funcionar hasta que agregues saldo. Te avisa antes.
