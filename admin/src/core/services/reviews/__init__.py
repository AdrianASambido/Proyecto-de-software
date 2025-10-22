"""
Este módulo representa las operaciones relacionadas con las reseñas de sitios históricos.
"""

from src.core.database import db
from src.core.Entities.review import Review, ReviewStatus
from src.core.Entities.site import Site
from src.core.Entities.user import User
from datetime import datetime
from sqlalchemy import or_, and_, desc, asc


def list_reviews(filtros: dict = None, page: int = 1, per_page: int = 25):
    """
    Retorna un objeto de paginación con las reseñas aplicando filtros y orden.
    """
    if filtros is None:
        filtros = {}
    query = filter_reviews(filtros)
    query = order_reviews(query, filtros)
    return query.paginate(page=page, per_page=per_page, error_out=False)


def filter_reviews(filtros: dict):
    """
    Filtra las reseñas según los filtros proporcionados.
    """
    query = Review.query.join(Site).join(User)

    # Filtro por estado
    estado = filtros.get("estado")
    if estado:
        if estado.upper() == "PENDIENTE":
            query = query.filter(Review.estado == ReviewStatus.PENDIENTE)
        elif estado.upper() == "APROBADA":
            query = query.filter(Review.estado == ReviewStatus.APROBADA)
        elif estado.upper() == "RECHAZADA":
            query = query.filter(Review.estado == ReviewStatus.RECHAZADA)

    # Filtro por sitio
    site_id = filtros.get("site_id")
    if site_id:
        query = query.filter(Review.site_id == int(site_id))

    # Filtro por calificación
    calificacion_min = filtros.get("calificacion_min")
    calificacion_max = filtros.get("calificacion_max")
    if calificacion_min:
        query = query.filter(Review.calificacion >= int(calificacion_min))
    if calificacion_max:
        query = query.filter(Review.calificacion <= int(calificacion_max))

    # Filtro por rango de fechas
    fecha_desde_str = filtros.get("fecha_desde")
    fecha_hasta_str = filtros.get("fecha_hasta")

    if fecha_desde_str:
        try:
            fecha_desde = datetime.strptime(fecha_desde_str, "%Y-%m-%d")
            query = query.filter(Review.created_at >= fecha_desde)
        except ValueError:
            pass

    if fecha_hasta_str:
        try:
            fecha_hasta = datetime.strptime(fecha_hasta_str, "%Y-%m-%d")
            query = query.filter(Review.created_at <= fecha_hasta)
        except ValueError:
            pass

    # Filtro por usuario (email)
    user_email = filtros.get("user_email")
    if user_email:
        query = query.filter(User.email.ilike(f"%{user_email}%"))

    return query


def order_reviews(query, filtros: dict):
    """
    Ordena las reseñas según el criterio especificado.
    """
    orden = filtros.get("order", "fecha_desc")
    opciones_orden = {
        "fecha_asc": Review.created_at.asc(),
        "fecha_desc": Review.created_at.desc(),
        "calificacion_asc": Review.calificacion.asc(),
        "calificacion_desc": Review.calificacion.desc(),
    }
    return query.order_by(opciones_orden.get(orden, Review.created_at.desc()))


def get_review(review_id: int):
    """
    Retorna una reseña por su ID.
    """
    return Review.query.get(review_id)

def get_all_sites():
    """
    Retorna todos los sitios para usar en el selector de filtros.
    """
    return Site.query.filter(Site.eliminated_at.is_(None)).order_by(Site.nombre).all()

def approve_review(review_id: int):
    """
    Aprueba una reseña cambiando su estado a APROBADA.
    """
    review = Review.query.get(review_id)
    if not review:
        raise ValueError(f"Reseña con ID {review_id} no encontrada")

    review.estado = ReviewStatus.APROBADA
    review.motivo_rechazo = None  # Limpiar motivo de rechazo si existía
    db.session.commit()
    return review


def reject_review(review_id: int, motivo: str):
    """
    Rechaza una reseña cambiando su estado a RECHAZADA.
    El motivo es obligatorio y debe tener máximo 200 caracteres.
    """
    if not motivo or len(motivo.strip()) == 0:
        raise ValueError("El motivo de rechazo es obligatorio")

    if len(motivo) > 200:
        raise ValueError("El motivo de rechazo no puede exceder los 200 caracteres")

    review = Review.query.get(review_id)
    if not review:
        raise ValueError(f"Reseña con ID {review_id} no encontrada")

    review.estado = ReviewStatus.RECHAZADA
    review.motivo_rechazo = motivo.strip()
    db.session.commit()
    return review


def delete_review(review_id: int):
    """
    Elimina una reseña de forma permanente.
    """
    review = Review.query.get(review_id)
    if not review:
        raise ValueError(f"Reseña con ID {review_id} no encontrada")

    db.session.delete(review)
    db.session.commit()
    return True
