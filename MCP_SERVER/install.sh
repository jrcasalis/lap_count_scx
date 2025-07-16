#!/bin/bash

echo "🚀 Instalando MCP Server para API Scalextric..."
echo "=" * 50

# Verificar si Python 3.8+ está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado. Por favor instala Python 3.8 o superior."
    exit 1
fi

# Verificar versión de Python
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python $python_version detectado"

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
python3 -m venv venv

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Crear archivo .env
echo "⚙️ Configurando variables de entorno..."
if [ ! -f .env ]; then
    cp env_example.txt .env
    echo "✅ Archivo .env creado. Edítalo con tu configuración."
else
    echo "✅ Archivo .env ya existe."
fi

echo ""
echo "🎉 ¡Instalación completada!"
echo ""
echo "📋 Próximos pasos:"
echo "1. Edita el archivo .env con tu configuración"
echo "2. Activa el entorno virtual: source venv/bin/activate"
echo "3. Ejecuta el servidor: python main.py"
echo "4. Prueba el cliente: python example_client.py"
echo ""
echo "🌐 Servidor disponible en: http://localhost:8000"
echo "📚 Documentación: http://localhost:8000/docs" 