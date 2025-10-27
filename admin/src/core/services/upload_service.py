# src/services/upload_service.py
import os
import uuid
from flask import current_app
from werkzeug.utils import secure_filename

def upload_file(file_storage, folder_name):
    """
    Sube un archivo a MinIO de forma segura.

    :param file_storage: El archivo (ej: request.files['portada']).
    :param folder_name: La carpeta en el bucket (ej: 'users' o 'sites').
    :return: El 'object_name' completo (ej: 'users/123e45-abc.jpg') 
             o None si el archivo está vacío o falla la subida.
    """
    
    # 1. Validar que el archivo exista
    if not file_storage or file_storage.filename == "":
        return None

    try:
        # 2. Crear un nombre de archivo SEGURO y ÚNICO
        # secure_filename() evita ataques de path traversal (ej: ../../etc/passwd)
        filename = secure_filename(file_storage.filename)
        # uuid.uuid4() evita que dos usuarios suban 'avatar.jpg' y se pisen
        unique_filename = f"{uuid.uuid4()}_{filename}"
        
        # 3. Construir el 'object_name' (la ruta completa en MinIO)
        object_name = f"{folder_name}/{unique_filename}"

        # 4. Obtener cliente, bucket y tamaño
        client = current_app.storage
        bucket_name = current_app.config["MINIO_BUCKET"]
        size = os.fstat(file_storage.fileno()).st_size
        file_storage.seek(0) # Aseguramos estar al inicio del archivo

        # 5. Subir a MinIO
        client.put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            data=file_storage,
            length=size,
            content_type=file_storage.content_type
        )

        current_app.logger.info(f"Archivo subido exitosamente: {object_name}")

        # 6. Devolver el nombre completo para guardarlo en la BD
        return object_name

    except Exception as e:
        current_app.logger.error(f"Error al subir archivo a MinIO: {e}")
        return None