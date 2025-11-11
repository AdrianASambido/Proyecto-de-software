# src/services/upload_service.py
import os
import uuid
from flask import current_app
from werkzeug.utils import secure_filename

def upload_file(file, folder_name):
    """
    Sube un archivo a MinIO de forma segura.

    :param folder_name: La carpeta en el bucket (ej: 'sites').
    :return: El 'object_name' completo (ej: 'sites/123e45-abc.jpg') 
             o None si el archivo está vacío o falla la subida.
    """
    
    if not file or file.filename == "":
        return None

    try:
        # Crear un nombre de archivo SEGURO y ÚNICO
        # secure_filename() evita ataques de path traversal (ej: ../../etc/passwd)
        filename = secure_filename(file.filename)
        # uuid.uuid4() evita que dos usuarios suban 'portada.jpg' y se pisen
        unique_filename = f"{uuid.uuid4()}_{filename}"
        
        # Construir el 'object_name' (la ruta completa en MinIO)
        object_name = f"{folder_name}/{unique_filename}"

        # Obtener cliente, bucket y tamaño
        client = current_app.storage
        bucket_name = current_app.config["MINIO_BUCKET"]
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0) # Aseguramos estar al inicio del archivo

        # Subir a MinIO
        client.put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            data=file,
            length=size,
            content_type=file.content_type
        )

        current_app.logger.info(f"Archivo subido exitosamente: {object_name}")

        return object_name

    except Exception as e:
        current_app.logger.error(f"Error al subir archivo a MinIO: {e}")
        return None


def delete_file(object_name: str):
    """
    Elimina un archivo de MinIO.

    :param object_name: El nombre del objeto completo (ej: 'sites/123e45-abc.jpg').
    :return: True si se eliminó correctamente, False en caso contrario.
    """
    if not object_name:
        return False

    try:
        client = current_app.storage
        bucket_name = current_app.config["MINIO_BUCKET"]
        
        client.remove_object(bucket_name=bucket_name, object_name=object_name)
        current_app.logger.info(f"Archivo eliminado exitosamente: {object_name}")
        return True

    except Exception as e:
        current_app.logger.error(f"Error al eliminar archivo de MinIO: {e}")
        return False