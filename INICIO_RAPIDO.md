# 🚀 INICIO RÁPIDO - Equipo de Marketing

## ✅ YA ESTÁ CONFIGURADO

- ✅ Entorno virtual Python creado
- ✅ Dependencias instaladas
- ✅ Scripts listos para usar
- ✅ Archivo .env preparado

## 📝 PASO 1: Configurar API Keys (5 minutos)

### Opción A: Editor nano (Recomendado)
```bash
cd ~/developers/agentes-org/backend
nano .env
```

**Reemplaza estas líneas:**
```
ANTHROPIC_API_KEY=your-anthropic-key-here  # ← Pega tu key de Anthropic
OPENAI_API_KEY=your-openai-key-here        # ← Pega tu key de OpenAI
```

**Guarda:** `Ctrl+O` → `Enter` → `Ctrl+X`

### Opción B: Usar VS Code
```bash
code ~/developers/agentes-org/backend/.env
```

**¿No tienes las keys?** Lee: `COMO_OBTENER_API_KEYS.md`

---

## 🚀 PASO 2: Iniciar el Dashboard

```bash
# Terminal 1 - Dashboard
cd ~/developers/agentes-org/dashboard
python3 -m http.server 8000
```

Abre: http://localhost:8000

---

## 🎬 PASO 3: Ejecutar Equipo de Marketing

```bash
# Terminal 2 - Ejecutar agentes
cd ~/developers/agentes-org/backend
./iniciar_marketing.sh
```

**Esto ejecuta:**
1. 🎨 Community Manager → Crea 7 posts
2. 🖼️ Diseñador Gráfico → Genera diseños con DALL-E
3. 📊 Analista → Analiza métricas
4. 💰 Paid Media → Planifica campañas
5. 📢 Gerente → Consolida reportes

**Tiempo estimado:** 2-3 minutos

---

## 👀 PASO 4: Ver y Aprobar Posts

1. Ve a: http://localhost:8000
2. Click en **"🏢 Espacios de Trabajo"**
3. Click en **"📢 Marketing"**
4. Verás **7 posts pendientes**

Cada post tiene:
- ✏️ Copy completo
- 🎨 Diseño generado (imagen)
- 📱 Plataformas (Instagram/Facebook)
- ⏰ Horario sugerido
- #️⃣ Hashtags

**Opciones:**
- ✅ **Aprobar** → Publica en redes sociales
- ❌ **Rechazar** → Descarta el post
- ✏️ **Editar** → Modifica antes de aprobar

---

## 🎯 MODO DE PRUEBA (Sin publicar realmente)

Por defecto está en **MOCK_MODE=true**:
- ✅ Genera todo el contenido
- ✅ Crea las imágenes
- ✅ Muestra en el workspace
- ⚠️ **NO publica** en redes sociales reales

**Para publicar de verdad:**
1. Configura tus tokens de Meta en `.env`
2. Cambia `MOCK_MODE=false` en `.env`
3. Reinicia el script

---

## 📂 ¿DÓNDE SE GUARDA TODO?

```
backend/
├── posts/
│   ├── pending/          ← Posts esperando aprobación
│   ├── approved/         ← Posts aprobados
│   ├── published/        ← Posts ya publicados ✅
│   └── rejected/         ← Posts rechazados ❌
│
├── assets/marketing/     ← Imágenes generadas 🎨
│
└── reportes/marketing/   ← Reportes de agentes 📊
```

---

## 🔄 COMANDOS ÚTILES

```bash
# Ver posts pendientes
ls backend/posts/pending/

# Ver imágenes generadas
ls backend/assets/marketing/

# Ver reportes
ls backend/reportes/marketing/*/

# Limpiar posts viejos
rm -rf backend/posts/*/*.json

# Ver logs
tail -f backend/logs/marketing.log
```

---

## ⚠️ SOLUCIÓN DE PROBLEMAS

### Error: "No API key found"
```bash
# Verifica que configuraste las keys
grep ANTHROPIC_API_KEY backend/.env
grep OPENAI_API_KEY backend/.env
```

### Error: "Module not found"
```bash
# Reactiva el entorno virtual
cd backend
source venv/bin/activate
pip list | grep anthropic
```

### No se generan imágenes
- Verifica que tengas `OPENAI_API_KEY` configurada
- Verifica que tengas créditos en OpenAI

### No aparecen posts en el workspace
1. Verifica que la API esté corriendo: `curl http://localhost:5000/api/marketing/status`
2. Si no está corriendo: `./start_marketing_api.sh`

---

## 📊 COSTOS ESTIMADOS

Por cada ejecución del workflow:
- **Claude (Anthropic):** ~$0.02 USD (generar contenido)
- **DALL-E (OpenAI):** ~$0.28 USD (7 imágenes)
- **Total:** ~$0.30 USD por ejecución

**Ejecución semanal:** ~$1.20/mes
**Ejecución diaria:** ~$9/mes

---

## 🎓 PRÓXIMOS PASOS

1. ✅ **Prueba el sistema** → Ejecuta y aprueba algunos posts
2. 📝 **Personaliza** → Edita los prompts en `backend/prompts/marketing/`
3. 🎨 **Ajusta diseños** → Modifica las specs de DALL-E
4. 🚀 **Activa publicación real** → Configura Meta y desactiva MOCK_MODE
5. 📊 **Revisa reportes** → Lee los insights del Analista

---

## ❓ ¿NECESITAS AYUDA?

**Documentación completa:**
- `COMO_OBTENER_API_KEYS.md` → Obtener tus API keys
- `COMO_FUNCIONA_REALMENTE.md` → Arquitectura del sistema
- `COMO_USAR_MARKETING.md` → Guía detallada de Marketing

**Soporte:**
- GitHub: https://github.com/hernanazocar/backoffice
- Issues: Abre un issue en el repo

---

## 🎉 ¡LISTO!

Ahora tienes un **equipo de Marketing con IA** completamente funcional.

**Comando para empezar:**
```bash
cd ~/developers/agentes-org/backend && ./iniciar_marketing.sh
```

🚀 **¡A crear contenido!**
