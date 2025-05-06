# Nuevo script para preparar modelos
import os
from transformers import DetrImageProcessor, DetrForObjectDetection
from pathlib import Path

def prepare_models():
    is_dev = os.getenv("ENV") == "dev"

    if is_dev:
        print("[DEBUG] Modo desarrollo activado. Se registrarán logs detallados.")

    try:
        if is_dev:
            print("[DEBUG] Iniciando preparación de modelos...")

        # Definir rutas coherentes con la estructura del proyecto
        models_dir = Path("src/models")
        models_dir.mkdir(parents=True, exist_ok=True)

        if is_dev:
            print(f"[DEBUG] Directorio de modelos creado o ya existente: {models_dir}")

        # Descargar y preparar el procesador
        processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
        processor.save_pretrained(models_dir / "detr-resnet-50-processor")

        if is_dev:
            print(f"[DEBUG] Procesador guardado en: {models_dir / 'detr-resnet-50-processor'}")

        # Descargar y preparar el modelo
        model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")
        model.save_pretrained(models_dir / "detr-resnet-50-model")

        if is_dev:
            print(f"[DEBUG] Modelo guardado en: {models_dir / 'detr-resnet-50-model'}")

        print("Modelos preparados y almacenados en src/models.")
    except Exception as e:
        if is_dev:
            print(f"[ERROR] Ocurrió un error durante la preparación de modelos: {e}")
        raise

if __name__ == "__main__":
    prepare_models()