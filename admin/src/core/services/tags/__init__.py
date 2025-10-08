from src.core.database import db
from src.core.Entities.tag import Tag
from datetime import date
import unicodedata
import re


def list_tags(filtros: dict | None = None):
    """Devuelve una consulta SQLAlchemy con los tags que cumplen los filtros dados."""
    if filtros is None:
        filtros = {}

    query = Tag.query.filter(Tag.deleted_at.is_(None))

    busqueda = filtros.get("busqueda")
    if busqueda:
        query = query.filter(Tag.name.ilike(f"%{busqueda}%"))

    orden = filtros.get("order", "fecha_desc")
    opciones_orden = {
        "fecha_asc": Tag.created_at.asc(),
        "fecha_desc": Tag.created_at.desc(),
        "nombre_asc": Tag.name.asc(),
        "nombre_desc": Tag.name.desc(),
    }
    query = query.order_by(opciones_orden[orden])

    return query


def add_tag(tag_data):
    """Crea una nueva etiqueta si no existe una con el mismo nombre."""
    new_tag = Tag(
        name=convert_to_lowercase(tag_data.get("nombre")),
        slug=generate_slug(tag_data.get("nombre")),
    )
    db.session.add(new_tag)
    db.session.commit()
    return new_tag


def update_tag(tag_id, tag_data):
    """Actualiza una etiqueta existente."""
    tag = Tag.query.get(tag_id)
    if not tag:
        return None

    tag.name = tag_data.get("nombre", tag.name)
    tag.slug = generate_slug(tag_data.get("nombre", tag.name))
    db.session.commit()
    return tag


def delete_tag(tag_id):
    """Elimina una etiqueta si no está asociada a ningún sitio."""
    tag = Tag.query.get(tag_id)
    if not tag:
        return None

    if tag.sites and len(tag.sites) > 0:
        raise ValueError(
            "No se puede eliminar una etiqueta que está asociada a sitios."
        )
        raise ValueError(
            "No se puede eliminar una etiqueta que está asociada a sitios."
        )

    tag.deleted_at = date.today()
    db.session.commit()
    return tag


def get_tag_by_id(tag_id):
    """
    retorna un tag por id
    """
    tag = Tag.query.get(tag_id)
    return tag


def get_tag_by_name(name):
    """
    retorna un tag por nombre
    """
    tag = Tag.query.filter_by(name=name, deleted_at=None).first()
    return tag


def convert_to_lowercase(text):
    return text.lower()


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
