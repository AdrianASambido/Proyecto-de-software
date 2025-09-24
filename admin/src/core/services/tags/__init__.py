from src.core.database import db
from src.core.Entities.tag import Tag
from datetime import date


def list_tags():
    tags = Tag.query.all()
    print(tags)

    return tags


def add_tag(tag_data):
    new_tag = Tag(
        nombre=tag_data.get("nombre"),
        slug=generate_slug(tag_data.get("nombre")),
        fecha_creacion=date.today(),
        # fecha_modificacion=date.today()
    )
    db.session.add(new_tag)
    db.session.commit()
    return new_tag


def update_tag(tag_id, tag_data):
    tag = Tag.query.get(tag_id)
    if not tag:
        return None

    tag.nombre = tag_data.get("nombre", tag.nombre)
    tag.slug = generate_slug(tag_data.get("nombre", tag.nombre))
    tag.fecha_creacion = tag.fecha_creacion
    tag.fecha_modificacion = date.today()

    db.session.commit()
    return tag


def delete_tag(tag_id):
    #db.session.delete(tag) cuando exista la base de datos
    #db.session.commit() cuando exista la base de datos
    return True


import unicodedata
import re


def generate_slug(name):
    # Normalizar caracteres (quitar acentos)
    slug = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    # Minusculas
    slug = slug.lower()
    # Reemplazar espacios y caracteres inválidos por guion
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    # Quitar guiones al inicio y fin
    slug = slug.strip("-")
    return slug


def get_tag_by_id(tag_id):
    return Tag.query.get(tag_id)