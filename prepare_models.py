# Nuevo script para preparar modelos
from transformers import DetrImageProcessor, DetrForObjectDetection
from pathlib import Path

def prepare_models():
    print("Descargando y preparando modelos...")

    # Definir rutas coherentes con la estructura del proyecto
    models_dir = Path("src/models")
    models_dir.mkdir(parents=True, exist_ok=True)

    # Descargar y preparar el procesador
    processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
    processor.save_pretrained(models_dir / "detr-resnet-50-processor")

    # Descargar y preparar el modelo
    model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")
    model.save_pretrained(models_dir / "detr-resnet-50-model")

    print("Modelos preparados y almacenados en src/models.")

if __name__ == "__main__":
    prepare_models()