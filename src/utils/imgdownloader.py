import requests
import os

def download_image(url, output_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(output_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        return output_path
    else:
        raise Exception(f"Error al descargar la imagen: {response.status_code}")