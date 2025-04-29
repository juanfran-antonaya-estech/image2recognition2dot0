from transformers import DetrImageProcessor, DetrForObjectDetection
from PIL import Image
import torch

def process_image_with_ai(image_path):
    # Cargar los modelos desde la carpeta local relativa a este archivo
    processor = DetrImageProcessor.from_pretrained("../models/detr-resnet-50-processor")
    model = DetrForObjectDetection.from_pretrained("../models/detr-resnet-50-model")

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

    return detections