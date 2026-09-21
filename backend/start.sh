#!/bin/bash

echo "🚀 Iniciando Sistema de Agentes IA..."

# Verificar si existe venv
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar venv
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -r requirements.txt --quiet

# Verificar .env
if [ ! -f ".env" ]; then
    echo "⚠️  Archivo .env no encontrado"
    echo "📝 Copiando .env.example a .env..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANTE: Edita el archivo .env y agrega tu ANTHROPIC_API_KEY"
    echo ""
    read -p "Presiona Enter cuando hayas configurado tu API key..."
fi

# Iniciar servidor
echo "🎯 Iniciando servidor FastAPI..."
python main.py
