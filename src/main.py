from utils.arggetter import get_arguments
from utils.imgdownloader import download_image
from utils.jfaltificial import process_image_with_ai
from utils.phototreater import treat_image
from utils.imgsender import authenticate_and_send_images
import os
from dotenv import load_dotenv
import requests
from PIL import Image
import logging

# Configurar el registro de mensajes
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Definir la ruta absoluta al directorio del procesador
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Cargar explícitamente el archivo .env desde el directorio raíz y forzar la sobreescritura
load_dotenv(dotenv_path=os.path.join(BASE_DIR, "..", ".env"), override=True)

LOGIN_URL = os.getenv("LOGIN_URL")
UPLOAD_URL = os.getenv("UPLOAD_URL")
SUBIMAGE_UPLOAD_URL = os.getenv("SUBIMAGE_UPLOAD_URL")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

if os.getenv("ENV") == "dev":
    print("DEPURACIÓN: LOGIN_URL:", LOGIN_URL)
    print("DEPURACIÓN: UPLOAD_URL:", UPLOAD_URL)
    print("DEPURACIÓN: EMAIL:", EMAIL)

# Reemplazar 127.0.0.1 con host.docker.internal para URLs si se ejecuta dentro de un contenedor
is_container = os.path.exists("/.dockerenv")
if is_container:
    if "127.0.0.1" in LOGIN_URL:
        LOGIN_URL = LOGIN_URL.replace("127.0.0.1", "host.docker.internal")
    if "127.0.0.1" in UPLOAD_URL:
        UPLOAD_URL = UPLOAD_URL.replace("127.0.0.1", "host.docker.internal")
    if "127.0.0.1" in SUBIMAGE_UPLOAD_URL:
        SUBIMAGE_UPLOAD_URL = SUBIMAGE_UPLOAD_URL.replace("127.0.0.1", "host.docker.internal")

def main():
    try:
        # Obtener argumentos
        url, image_id, mode = get_arguments()

        # Descargar imagen
        image_path = f"temp_image_{image_id}.jpg"
        download_image(url, image_path)

        # Procesar imagen con IA
        detections = process_image_with_ai(image_path)

        # Tratar imagen
        modified_image, sub_images = treat_image(image_path, detections)
        modified_image_path = f"modified_image_{image_id}.png"
        modified_image.save(modified_image_path)

        # Guardar subimágenes en archivos temporales con nombres únicos
        # Depuración: Verificar la creación y existencia de archivos
        temp_sub_images = []
        for idx, (sub_image, label, score) in enumerate(sub_images):
            if isinstance(sub_image, Image.Image):
                temp_sub_image_path = f"temp_sub_image_{image_id}_{label}_{idx}.png"
                sub_image.save(temp_sub_image_path)
                if os.path.exists(temp_sub_image_path):
                    logger.debug(f"Archivo creado exitosamente: {temp_sub_image_path}")
                else:
                    logger.error(f"Fallo en la creación del archivo: {temp_sub_image_path}")
                temp_sub_images.append((temp_sub_image_path, label, score))
            else:
                temp_sub_images.append((sub_image, label, score))

        # Enviar datos al backend
        credentials = {"email": EMAIL, "password": PASSWORD}
        authenticate_and_send_images(modified_image_path, temp_sub_images, image_id, LOGIN_URL, UPLOAD_URL, credentials)

        # Asegurarse de que la limpieza ocurra solo después de que todas las operaciones se completen
        try:
            # Enviar subimágenes
            for temp_sub_image_path, label, score in temp_sub_images:
                with open(temp_sub_image_path, "rb") as img_file:
                    response = requests.post(SUBIMAGE_UPLOAD_URL, headers=headers, files={"image": img_file}, data={"id": image_id, "objeto": label, "seguridad": score})
                    if response.status_code != 200:
                        raise Exception("Error al enviar una subimagen")
        finally:
            # Limpiar archivos temporales de subimágenes
            for temp_sub_image_path, _, _ in temp_sub_images:
                if os.path.exists(temp_sub_image_path):
                    os.remove(temp_sub_image_path)

            # Limpiar archivos temporales
            if os.path.exists(image_path):
                os.remove(image_path)
            if os.path.exists(modified_image_path):
                os.remove(modified_image_path)

        print(True)
    except Exception as e:
        print(f"Error: {e}")
        print(False)

if __name__ == "__main__":
    main()