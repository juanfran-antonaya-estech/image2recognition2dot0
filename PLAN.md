# PLAN DE APLICACIÓN

Esta aplicación es para recoger por argumentos un enlace, una id que es la imagen original y un modo (editar | crear)
---
- main.py
    - Se encarga de conducir el flujo de la aplicación entre los utils
- arggetter.py
    - Se encarga de recoger los argumentos pasados por comando de terminal que son, en orden:
        1. url de la imagen original
        1. id (integer) de la imagen original
        1. modo de procesado (crear | editar) (en esta versión solo está crear, tras la siguiente será ambas funciones)
- imgdownloader.py
    - Se encarga de descargarse de la url de la imagen proporcionado por arggetter la imagen que va a devolver para ser procesada por el procesador
- jfaltificial.py (modelo detr-resnet-50 de huggingface)
    - Se encarga de realizar el procesado de la imagen por inteligencia artificial, sacando las coordenadas, objeto y la accuracy de todos los objetos reconocidos en la imagen para poder ser pasados a phototreater
- phototreater.py
    - Recibe los datos de jfaltificial para realizar dos acciones:
        1. De una copia de la imagen original dibuja rectángulos de color rojo en las coordenadas marcadas por la inteligencia artificial marcando también el objeto y la accuracy.
        1. copia regiones de la foto original definidas por las coordenadas de jfaltificial para crear un array de imagenes y poder enviarlas como subimágenes
- imgsender.py
    - primero debe iniciar sesion con usuarios y contraseñas y sacar un bearer token, este es un ejemplo del body que tiene que enviar al endpoint de login
    ```json
    {
    "email":"destany.effertz@example.net",
    "password":"password"
    }    
    ```
    La respuesta, si es un 200, el campo que tiene que sacar el token se llama "token", poniendo esa autenticación de bearer token ya se puede comunicar con el backend
    - Tiene dos tipos de envío, aunque realiza ambos:
        - ImagenModificada:
            Envia al endpoint del backend un post conteniendo los siguientes datos
            ```json
            {
                "image": "la imagen modificada, debe ser formato png",
                "id": "la id de la imagen original"
            }
            ```
            ovbiamente hay que enviarle al backend la imagen
        - SubImagen:
            Envia al Backend una petición por imagen en el array de subimágenes (el backend no tiene limite para este script), los datos que tiene que tener el body del post es:
            ```json
            {
                "image": "la subimagen(debe ser formato png)",
                "id": "Id de la imagen original",
                "objeto": "nombre del objeto reconocido por el procesador",
                "seguridad":"accuracy del objeto reconocido por el procesador"
            }
            ```

tras realizar el proceso completo, la aplicación debe solar un true o un false dependiendo de si ha ido bien o no, así laravel sabrá que el script ha acabado y seguirá realizando sus tareas.

---

## Pasos para seguir la estructura del plan

1. **Identificar el flujo principal**:
   - El archivo `main.py` es el encargado de coordinar el flujo entre los módulos en `utils/`.
   - Asegúrate de que cada módulo esté correctamente integrado y que el flujo de datos entre ellos sea claro.

2. **Recolectar argumentos**:
   - El módulo `arggetter.py` debe recoger los argumentos de entrada: URL de la imagen, ID de la imagen, y el modo de procesado (`crear` o `editar`).
   - Verifica que los argumentos sean válidos y maneja errores si no lo son.

3. **Descargar la imagen**:
   - Usa `imgdownloader.py` para descargar la imagen desde la URL proporcionada.
   - Asegúrate de manejar errores de red o de URL inválida.

4. **Procesar la imagen con IA**:
   - El módulo `jfaltificial.py` utiliza el modelo `detr-resnet-50` de Hugging Face para procesar la imagen.
   - Extrae las coordenadas, el objeto reconocido y la precisión (accuracy) de cada objeto.

5. **Tratar la imagen**:
   - Usa `phototreater.py` para:
     - Dibujar rectángulos en la imagen original con los datos proporcionados por `jfaltificial.py`.
     - Crear un array de subimágenes basadas en las coordenadas detectadas.

6. **Enviar datos al backend**:
   - Usa `imgsender.py` para:
     - Iniciar sesión y obtener un token de autenticación.
     - Enviar la imagen modificada al backend con el formato especificado.
     - Enviar cada subimagen al backend con los datos correspondientes (objeto, precisión, etc.).

7. **Finalizar el proceso**:
   - La aplicación debe devolver `true` o `false` dependiendo de si el proceso fue exitoso.
   - Esto permitirá que Laravel continúe con sus tareas.

8. **Validar y probar**:
   - Asegúrate de que cada módulo funcione de manera independiente y en conjunto.
   - Realiza pruebas para verificar que el flujo completo funcione correctamente.

9. **Documentar cambios**:
   - Actualiza el archivo `PLAN.md` si se realizan modificaciones en el flujo o en los módulos.

## Pruebas y Tests

### Funcionalidades a Probar
1. **Recolección de Argumentos**: Verificar que `arggetter.py` maneje correctamente los argumentos válidos e inválidos.
2. **Descarga de Imágenes**: Probar que `imgdownloader.py` descargue imágenes correctamente desde URLs válidas y maneje errores en URLs inválidas.
3. **Procesamiento con IA**: Asegurarse de que `jfaltificial.py` detecte objetos correctamente en imágenes de prueba.
4. **Tratamiento de Imágenes**: Validar que `phototreater.py` dibuje correctamente los rectángulos y genere subimágenes.
5. **Envío de Imágenes**: Comprobar que `imgsender.py` autentique y envíe imágenes y subimágenes a los endpoints correctos.
6. **Flujo Principal**: Probar el flujo completo en `main.py` con diferentes combinaciones de argumentos y escenarios.

### Casos de Prueba
- Argumentos faltantes o inválidos.
- URLs de imágenes no válidas o inaccesibles.
- Imágenes con diferentes resoluciones y formatos.
- Respuestas del backend con errores (autenticación fallida, errores 500, etc.).

### Observaciones
- ...
### Cosas a mejorar
- Se queda atascado en una conexión con el servidor