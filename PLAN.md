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

### Observaciones
- ...
### Cosas a mejorar
- Va piola