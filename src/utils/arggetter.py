import sys

def get_arguments():
    if len(sys.argv) != 4:
        raise ValueError("Se requieren exactamente 3 argumentos: URL, ID y modo (crear | editar)")

    url = sys.argv[1]
    try:
        image_id = int(sys.argv[2])
    except ValueError:
        raise ValueError("El ID debe ser un número entero")

    mode = sys.argv[3]
    if mode not in ["crear", "editar"]:
        raise ValueError("El modo debe ser 'crear' o 'editar'")

    return url, image_id, mode