# Image2Recognition 2.0

## Descripción
Image2Recognition 2.0 es una aplicación basada en Python diseñada para procesar imágenes utilizando inteligencia artificial, extraer datos de objetos y enviar los datos procesados a un servidor backend. Se integra con aplicaciones Laravel y utiliza el modelo `detr-resnet-50` de Hugging Face para la detección de objetos.

## Características
- Descarga imágenes desde una URL proporcionada.
- Procesa imágenes utilizando IA para detectar objetos, sus coordenadas y niveles de confianza.
- Modifica la imagen dibujando cuadros delimitadores y etiquetas.
- Extrae subimágenes basadas en los objetos detectados.
- Envía la imagen modificada y las subimágenes a un servidor backend.

## Requisitos
- Python 3.8+
- Librerías listadas en `requirements.txt`
- Docker (opcional, para despliegue en contenedores)

## Configuración

### Configuración Local
1. Clona el repositorio:
   ```bash
   git clone <repository-url>
   cd image2recognition2dot0
   ```
2. Configura un entorno virtual e instala las dependencias:
   ```bash
   setup_env.bat
   ```
3. Configura las variables de entorno:
   - Copia `.env.example` a `.env` y completa los valores requeridos.

4. Prepara los modelos:
   ```bash
   python prepare_models.py
   ```

### Configuración con Docker
1. Construye la imagen de Docker:
   ```bash
   docker build -t image2recognition2dot0 .
   ```
2. Ejecuta el contenedor:
   ```bash
   docker run --env-file .env image2recognition2dot0
   ```

## Uso
Ejecuta la aplicación con el siguiente comando:
```bash
python src/main.py <image_url> <image_id> <mode>
```
- `<image_url>`: URL de la imagen a procesar.
- `<image_id>`: ID entero de la imagen.
- `<mode>`: Modo de procesamiento (`crear` o `editar`).

## Pruebas
Consulta `PLAN.md` para casos de prueba y escenarios detallados.