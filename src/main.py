from utils.arggetter import get_arguments
from utils.imgdownloader import download_image
from utils.jfaltificial import process_image_with_ai
from utils.phototreater import treat_image
from utils.imgsender import authenticate_and_send_images
import os
from dotenv import load_dotenv
import requests

# Cargar variables de entorno
load_dotenv()

LOGIN_URL = os.getenv("LOGIN_URL")
UPLOAD_URL = os.getenv("UPLOAD_URL")
SUBIMAGE_UPLOAD_URL = os.getenv("SUBIMAGE_UPLOAD_URL")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

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

        # Enviar datos al backend
        credentials = {"email": EMAIL, "password": PASSWORD}
        authenticate_and_send_images(modified_image_path, sub_images, image_id, LOGIN_URL, UPLOAD_URL, credentials)

        # Enviar subimágenes
        for sub_image, label, score in sub_images:
            with open(sub_image, "rb") as img_file:
                response = requests.post(SUBIMAGE_UPLOAD_URL, headers=headers, files={"image": img_file}, data={"id": image_id, "objeto": label, "seguridad": score})
                if response.status_code != 200:
                    raise Exception("Error al enviar una subimagen")

        # Limpiar archivos temporales
        os.remove(image_path)
        os.remove(modified_image_path)

        print(True)
    except Exception as e:
        print(f"Error: {e}")
        print(False)

if __name__ == "__main__":
    main()