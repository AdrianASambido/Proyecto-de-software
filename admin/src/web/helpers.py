from flask import current_app

def cover_url(cover):
    """Genera la URL de la portada de un sitio."""
    if cover is None:
        return None
    
    client = current_app.storage
    return client.presigned_get_object(
        bucket_name=current_app.config["MINIO_BUCKET"],
        object_name=cover,
    )


def image_url(image):
    """Genera la URL de una imagen."""
    if image is None:
        return None
    
    client = current_app.storage
    return client.presigned_get_object(
        bucket_name=current_app.config["MINIO_BUCKET"],
        object_name=image,
    )