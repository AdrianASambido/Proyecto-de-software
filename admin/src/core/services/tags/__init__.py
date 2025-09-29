from src.core.database import db
from src.core.Entities.tag import Tag
from datetime import date
import unicodedata
import re


def list_tags():
    tags = Tag.query.filter_by(deleted_at=None).all()
    return tags


def add_tag(tag_data):
    new_tag = Tag(
        name=tag_data.get("nombre"),
        slug=generate_slug(tag_data.get("nombre")),
    )
    db.session.add(new_tag)
    db.session.commit()
    return new_tag


def update_tag(tag_id, tag_data):
    tag = Tag.query.get(tag_id)
    if not tag:
        return None

    tag.name = tag_data.get("nombre", tag.name)
    tag.slug = generate_slug(tag_data.get("nombre", tag.name))
    db.session.commit()
    return tag


def delete_tag(tag_id):
    # elimnacion logica
    tag = Tag.query.get(tag_id)
    if not tag:
        return None

    tag.deleted_at = date.today()
    db.session.commit()
    return tag


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
    tag = Tag.query.get(tag_id)
    return tag
