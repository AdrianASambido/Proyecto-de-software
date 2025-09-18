from core.Entities.tag import Tag, db
from datetime import date

tags= [
    {
        "id": 1,
        "nombre": "Maravillas del Mundo",
        "slug": "maravillas-del-mundo",
    }
]
def get_tags():
    """
    Retorna una lista de todos los tags.
    """
    #tags=Tag.query.all() cuando exista la base de datos
    
    return tags

def add_tag(tag_data):
    nuevo_tag = {
        "id": 3,  
        "nombre": tag_data.get("nombre"),
        "slug": generate_slug(tag_data.get("nombre")),
        "fecha_creacion": date.today(),
    }
    #db.session.add(nuevo_tag) cuando exista la base de datos
    #db.session.commit() cuando exista la base de datos
    tags.append(nuevo_tag)
    return nuevo_tag


import unicodedata
import re

def generate_slug(name):
    # Normalizar caracteres (quitar acentos)
    slug = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    # Minusculas
    slug = slug.lower()
    # Reemplazar espacios y caracteres inválidos por guion
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    # Quitar guiones al inicio y fin
    slug = slug.strip('-')
    return slug
