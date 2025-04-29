# setup_env.bat
@echo off
python -m venv venv
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
call venv\Scripts\activate
python prepare_models.py
@echo Entorno virtual configurado, dependencias instaladas y modelos preparados.