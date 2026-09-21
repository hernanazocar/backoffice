#!/bin/bash

# Script para iniciar el equipo de Marketing fácilmente

echo "🚀 Iniciando Equipo de Marketing..."
echo ""

# Activar entorno virtual
source venv/bin/activate

# Verificar que las API keys estén configuradas
if grep -q "your-anthropic-key-here" .env; then
    echo "⚠️  ATENCIÓN: Necesitas configurar tus API keys"
    echo ""
    echo "1. Abre el archivo .env:"
    echo "   nano .env"
    echo ""
    echo "2. Reemplaza 'your-xxx-key-here' con tus keys reales"
    echo ""
    echo "3. Guía completa: cat ../COMO_OBTENER_API_KEYS.md"
    echo ""
    read -p "Presiona Enter cuando hayas configurado las keys..."
fi

# Ejecutar el workflow de marketing
echo ""
echo "✨ Ejecutando agentes de Marketing..."
echo ""
python3 ejecutar_workflow.py marketing

echo ""
echo "✅ ¡Listo! Ahora abre:"
echo "   http://localhost:8000"
echo ""
echo "Y ve a: Espacios de Trabajo → Marketing"
