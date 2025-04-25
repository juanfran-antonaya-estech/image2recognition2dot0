from PIL import Image, ImageDraw

def treat_image(image_path, detections):
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

    return image, sub_images