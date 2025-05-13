import requests
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def download_image(url, output_path):
    is_dev = os.getenv("ENV") == "dev"

    try:
        if is_dev:
            logger.debug(f"Iniciando descarga de imagen desde URL: {url}")

        response = requests.get(url, stream=True, timeout=300)
        if response.status_code == 200:
            with open(output_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            if is_dev:
                logger.debug(f"Imagen descargada y guardada en: {output_path}")
            return output_path
        else:
            error_message = f"Error al descargar la imagen: {response.status_code}"
            if is_dev:
                logger.error(error_message)
            raise Exception(error_message)
    except Exception as e:
        if is_dev:
            logger.error(f"Excepción durante la descarga de la imagen: {e}")
        raise