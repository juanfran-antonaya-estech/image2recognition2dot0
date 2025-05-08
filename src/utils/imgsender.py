import os
import requests
import logging
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from PIL import Image

# Configurar el registro de mensajes
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configurar la estrategia de reintento
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]  # Actualizado de method_whitelist a allowed_methods
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session = requests.Session()
session.mount("https://", adapter)
session.mount("http://", adapter)

def authenticate_and_send_images(modified_image_path, sub_images, image_id, login_url, upload_url, credentials):
    is_dev = os.getenv("ENV") == "dev"

    try:
        if is_dev:
            logger.debug("Iniciando autenticación...")
            logger.debug(f"URL de solicitud: {login_url}")
            logger.debug(f"Carga útil de solicitud: {credentials}")

        # Agregar encabezados para la solicitud de autenticación
        auth_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        if is_dev:
            logger.debug(f"Encabezados de solicitud: {auth_headers}")

        # Autenticación
        auth_response = session.post(login_url, json=credentials, headers=auth_headers, timeout=10)

        if is_dev:
            logger.debug(f"Código de estado de respuesta: {auth_response.status_code}")
            logger.debug(f"Cuerpo de respuesta: {auth_response.text}")

        if auth_response.status_code != 200:
            error_message = "Error al autenticar"
            if is_dev:
                logger.error(error_message)
            raise Exception(error_message)

        token = auth_response.json().get("token")
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"  # Agregado encabezado Accept
        }

        if is_dev:
            logger.debug("Autenticación exitosa. Token obtenido.")

        # Asegurarse de que la imagen modificada esté guardada en un archivo antes de enviarla
        if isinstance(modified_image_path, Image.Image):
            temp_image_path = f"temp_modified_image_{image_id}.png"
            modified_image_path.save(temp_image_path)
            modified_image_path = temp_image_path

        # Asegurarse de que todas las subimágenes estén guardadas en archivos temporales antes de enviarlas
        temp_sub_images = []
        for sub_image, label, score in sub_images:
            if isinstance(sub_image, Image.Image):
                temp_sub_image_path = f"temp_sub_image_{image_id}_{label}.png"
                sub_image.save(temp_sub_image_path)
                temp_sub_images.append((temp_sub_image_path, label, score))
            else:
                temp_sub_images.append((sub_image, label, score))

        # Reemplazar sub_images con temp_sub_images para un procesamiento posterior
        sub_images = temp_sub_images

        # Enviar imagen modificada
        with open(modified_image_path, "rb") as img_file:
            response = session.post(upload_url, headers=headers, files={"image": img_file}, data={"id": image_id}, timeout=10)
            if response.status_code != 200:
                error_message = "Error al enviar la imagen modificada"
                if is_dev:
                    logger.error(error_message)
                raise Exception(error_message)

        if is_dev:
            logger.debug(f"Imagen modificada enviada correctamente: {modified_image_path}")

        # Enviar subimágenes y eliminar después de un envío exitoso
        for sub_image, label, score in sub_images:
            with open(sub_image, "rb") as img_file:
                response = session.post(upload_url, headers=headers, files={"image": img_file}, data={"id": image_id, "objeto": label, "seguridad": score}, timeout=10)
                if response.status_code != 200:
                    error_message = f"Error al enviar una subimagen: {sub_image}"
                    if is_dev:
                        logger.error(error_message)
                    raise Exception(error_message)

                if is_dev:
                    logger.debug(f"Subimagen enviada correctamente: {sub_image}")

            # Eliminar el archivo después de asegurarse de que esté cerrado
            if os.path.exists(sub_image):
                try:
                    os.remove(sub_image)
                    if is_dev:
                        logger.debug(f"Archivo eliminado después de un envío exitoso: {sub_image}")
                except Exception as e:
                    if is_dev:
                        logger.error(f"No se pudo eliminar el archivo {sub_image}: {e}")

            # Introducir un pequeño retraso entre solicitudes
            time.sleep(0.5)

        # Limpiar archivos temporales solo después de que todas las operaciones estén completas
        temp_files = []
        if 'temp_image_path' in locals():
            temp_files.append(temp_image_path)

        for sub_image, _, _ in sub_images:
            temp_files.append(sub_image)

        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    except Exception as e:
        if is_dev:
            logger.error(f"Error en el proceso de envío de imágenes: {e}")
        raise