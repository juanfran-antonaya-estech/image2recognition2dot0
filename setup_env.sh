#!/bin/bash

# Crear un entorno virtual
python3 -m venv venv

# Activar el entorno virtual
source venv/bin/activate

# instalar dependencias
pip pip install --no-cache-dir --upgrade pip
pip install --no-cache-dir -r requirements.txt

# Preparar los modelos
python prepare_models.py

echo "Entorno virtual configurado, dependencias instaladas y modelos preparados."