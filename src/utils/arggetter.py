import sys
import os
import logging

# Configurar el registro de mensajes
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_arguments():
    # Recoger argumentos pasados por la línea de comandos
    is_dev = os.getenv("ENV") == "dev"
    is_container = os.path.exists("/.dockerenv")  # Comprobar si se está ejecutando dentro de un contenedor

    if len(sys.argv) != 4:
        error_message = "Se requieren exactamente 3 argumentos: URL, ID y modo (crear | editar)"
        if is_dev:
            logger.error(error_message)
        raise ValueError(error_message)

    url = sys.argv[1]
    # Reemplazar 127.0.0.1 con host.docker.internal solo si se ejecuta dentro de un contenedor
    if is_container and "127.0.0.1" in url:
        url = url.replace("127.0.0.1", "host.docker.internal")

    try:
        image_id = int(sys.argv[2])
    except ValueError:
        error_message = "El ID debe ser un número entero"
        if is_dev:
            logger.error(error_message)
        raise ValueError(error_message)

    mode = sys.argv[3]
    if mode not in ["crear", "editar"]:
        error_message = "El modo debe ser 'crear' o 'editar'"
        if is_dev:
            logger.error(error_message)
        raise ValueError(error_message)

    if is_dev:
        logger.debug(f"Argumentos recibidos: URL={url}, ID={image_id}, Modo={mode}")

    return url, image_id, mode