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
        print(f"Argumentos obtenidos: url={url}, image_id={image_id}, mode={mode}")

        # Descargar imagen
        image_path = f"temp_image_{image_id}.jpg"
        download_image(url, image_path)
        print(f"Imagen descargada en: {image_path}")

        # Procesar imagen con IA
        detections = process_image_with_ai(image_path)
        print(f"Detecciones obtenidas: {detections}")

        # Tratar imagen
        modified_image, sub_images = treat_image(image_path, detections)
        print(f"Imagen tratada. Subimágenes generadas: {len(sub_images)}")
        modified_image_path = f"modified_image_{image_id}.png"
        modified_image.save(modified_image_path)
        print(f"Imagen modificada guardada en: {modified_image_path}")

        # Guardar subimágenes en archivos temporales con nombres únicos
        temp_sub_images = []
        for idx, (sub_image, label, score) in enumerate(sub_images):
            if isinstance(sub_image, Image.Image):
                temp_sub_image_path = f"temp_sub_image_{image_id}_{label}_{idx}.png"
                sub_image.save(temp_sub_image_path)
                if os.path.exists(temp_sub_image_path):
                    print(f"Archivo creado exitosamente: {temp_sub_image_path}")
                else:
                    print(f"Fallo en la creación del archivo: {temp_sub_image_path}")
                temp_sub_images.append((temp_sub_image_path, label, score))
            else:
                print(f"Subimagen no es una instancia de Image.Image: {sub_image}")
                temp_sub_images.append((sub_image, label, score))

        # Enviar datos al backend
        credentials = {"email": EMAIL, "password": PASSWORD}
        print(f"Credenciales preparadas para autenticación: {credentials}")
        authenticate_and_send_images(modified_image_path, temp_sub_images, image_id, LOGIN_URL, UPLOAD_URL, credentials)

        # Asegurarse de que la limpieza ocurra solo después de que todas las operaciones se completen
        if os.path.exists(image_path):
            os.remove(image_path)
            print(f"Archivo temporal eliminado: {image_path}")
        if os.path.exists(modified_image_path):
            os.remove(modified_image_path)
            print(f"Archivo temporal eliminado: {modified_image_path}")

    except Exception as e:
        print(f"Error en el flujo principal: {e}")
        print(False)
    finally:
        print(True)

if __name__ == "__main__":
    main()