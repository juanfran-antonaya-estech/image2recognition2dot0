import os
import logging
from transformers import DetrImageProcessor, DetrForObjectDetection
from PIL import Image
import torch

# Configurar logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def process_image_with_ai(image_path):
    is_dev = os.getenv("ENV") == "dev"

    try:
        if is_dev:
            logger.debug(f"Procesando imagen con IA: {image_path}")

        # Definir rutas absolutas para los modelos
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        PROCESSOR_PATH = os.path.join(BASE_DIR, "..", "models", "detr-resnet-50-processor")
        MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "detr-resnet-50-model")

        # Cargar los modelos desde las rutas absolutas
        processor = DetrImageProcessor.from_pretrained(PROCESSOR_PATH)
        model = DetrForObjectDetection.from_pretrained(MODEL_PATH)

        image = Image.open(image_path).convert("RGB")
        inputs = processor(images=image, return_tensors="pt")

        outputs = model(**inputs)
        target_sizes = torch.tensor([image.size[::-1]])
        results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

        detections = []
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            detections.append({
                "score": score.item(),
                "label": model.config.id2label[label.item()],
                "box": box.tolist()
            })

        if is_dev:
            logger.debug(f"Detecciones realizadas: {detections}")

        return detections
    except Exception as e:
        if is_dev:
            logger.error(f"Error al procesar la imagen con IA: {e}")
        raise