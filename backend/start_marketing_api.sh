#!/bin/bash

# Script para iniciar la API de Marketing

echo "🚀 Iniciando Sistema de Marketing..."
echo ""

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ Entorno virtual activado"
fi

# Verificar que existan las dependencias
if ! python3 -c "import flask" 2>/dev/null; then
    echo "⚠️  Instalando dependencias..."
    pip install -r requirements-marketing.txt
fi

# Crear directorios necesarios
mkdir -p ../posts/pending
mkdir -p ../posts/approved
mkdir -p ../posts/published
mkdir -p ../posts/rejected
mkdir -p ../assets/marketing

echo "✓ Directorios creados"
echo ""

# Iniciar API
echo "🌐 Iniciando API en http://localhost:5000"
echo "📊 Dashboard en http://localhost:8000"
echo ""
echo "Presiona Ctrl+C para detener"
echo ""

python3 api/marketing_api.py
