from datetime import datetime, timezone
from src.core.database import db
import enum


class ReviewStatus(enum.Enum):
    PENDIENTE = "pendiente"
    APROBADA = "aprobada"
    RECHAZADA = "rechazada"


class Review(db.Model):
    """
    Modelo que representa una reseña de un sitio histórico creada por un usuario público
    """

    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    site_id = db.Column(db.Integer, db.ForeignKey("sites.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    calificacion = db.Column(db.Integer, nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    estado = db.Column(db.Enum(ReviewStatus), nullable=False, default=ReviewStatus.PENDIENTE)
    motivo_rechazo = db.Column(db.String(200), nullable=True)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # Relaciones
    site = db.relationship("Site", backref="reviews", lazy="select")
    user = db.relationship("User", backref="reviews", lazy="select")

    def __repr__(self):
        return f"<Review {self.id} | Site: {self.site_id} | User: {self.user_id} | Rating: {self.calificacion}>"

    def to_dict(self):
        return {
            "id": self.id,
            "site_id": self.site_id,
            "user_id": self.user_id,
            "calificacion": self.calificacion,
            "contenido": self.contenido,
            "estado": self.estado.value if self.estado else None,
            "motivo_rechazo": self.motivo_rechazo,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
