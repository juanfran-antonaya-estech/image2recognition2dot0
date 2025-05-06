import os
import requests
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def authenticate_and_send_images(modified_image_path, sub_images, image_id, login_url, upload_url, credentials):
    is_dev = os.getenv("ENV") == "dev"

    try:
        if is_dev:
            logger.debug("Iniciando autenticación...")

        # Autenticación
        auth_response = requests.post(login_url, json=credentials)
        if auth_response.status_code != 200:
            error_message = "Error al autenticar"
            if is_dev:
                logger.error(error_message)
            raise Exception(error_message)

        token = auth_response.json().get("token")
        headers = {"Authorization": f"Bearer {token}"}

        if is_dev:
            logger.debug("Autenticación exitosa. Token obtenido.")

        # Enviar imagen modificada
        with open(modified_image_path, "rb") as img_file:
            response = requests.post(upload_url, headers=headers, files={"image": img_file}, data={"id": image_id})
            if response.status_code != 200:
                error_message = "Error al enviar la imagen modificada"
                if is_dev:
                    logger.error(error_message)
                raise Exception(error_message)

        if is_dev:
            logger.debug(f"Imagen modificada enviada correctamente: {modified_image_path}")

        # Enviar subimágenes
        for sub_image, label, score in sub_images:
            with open(sub_image, "rb") as img_file:
                response = requests.post(upload_url, headers=headers, files={"image": img_file}, data={"id": image_id, "objeto": label, "seguridad": score})
                if response.status_code != 200:
                    error_message = f"Error al enviar una subimagen: {sub_image}"
                    if is_dev:
                        logger.error(error_message)
                    raise Exception(error_message)

            if is_dev:
                logger.debug(f"Subimagen enviada correctamente: {sub_image}")

    except Exception as e:
        if is_dev:
            logger.error(f"Error en el proceso de envío de imágenes: {e}")
        raise