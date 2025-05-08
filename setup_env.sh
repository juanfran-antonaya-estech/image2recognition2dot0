#!/bin/bash

# Crear un entorno virtual
python3 -m venv venv

# Activar el entorno virtual
source venv/bin/activate

# Actualizar pip e instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Preparar los modelos
python prepare_models.py

echo "Entorno virtual configurado, dependencias instaladas y modelos preparados."