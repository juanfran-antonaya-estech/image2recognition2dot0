import requests

def authenticate_and_send_images(modified_image_path, sub_images, image_id, login_url, upload_url, credentials):
    # Autenticación
    auth_response = requests.post(login_url, json=credentials)
    if auth_response.status_code != 200:
        raise Exception("Error al autenticar")

    token = auth_response.json().get("token")
    headers = {"Authorization": f"Bearer {token}"}

    # Enviar imagen modificada
    with open(modified_image_path, "rb") as img_file:
        response = requests.post(upload_url, headers=headers, files={"image": img_file}, data={"id": image_id})
        if response.status_code != 200:
            raise Exception("Error al enviar la imagen modificada")

    # Enviar subimágenes
    for sub_image, label, score in sub_images:
        with open(sub_image, "rb") as img_file:
            response = requests.post(upload_url, headers=headers, files={"image": img_file}, data={"id": image_id, "objeto": label, "seguridad": score})
            if response.status_code != 200:
                raise Exception("Error al enviar una subimagen")