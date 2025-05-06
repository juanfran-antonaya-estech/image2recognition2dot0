import logging
import os
from PIL import Image, ImageDraw

# Configurar logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def treat_image(image_path, detections):
    is_dev = os.getenv("ENV") == "dev"

    try:
        if is_dev:
            logger.debug(f"Tratando imagen: {image_path} con detecciones: {detections}")

        image = Image.open(image_path).convert("RGB")
        draw = ImageDraw.Draw(image)

        sub_images = []
        for detection in detections:
            box = detection["box"]
            label = detection["label"]
            score = detection["score"]

            # Dibujar rectángulos
            draw.rectangle(box, outline="red", width=3)
            draw.text((box[0], box[1]), f"{label} ({score:.2f})", fill="red")

            # Crear subimágenes
            cropped_image = image.crop(box)
            sub_images.append((cropped_image, label, score))

        if is_dev:
            logger.debug(f"Imagen tratada y subimágenes generadas: {len(sub_images)} subimágenes")

        return image, sub_images
    except Exception as e:
        if is_dev:
            logger.error(f"Error al tratar la imagen: {e}")
        raise