from src.core.database import db
from datetime import datetime, timezone
from geoalchemy2.types import Geometry
from geoalchemy2.shape import to_shape
from src.core.Entities.tag import site_tags
from src.core.Entities.image import Image


class Site(db.Model):
    """
    Modelo que representa un sitio historico en la base de datos
    """

    __tablename__ = "sites"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion_breve = db.Column(db.Text, nullable=False)
    descripcion_completa = db.Column(db.Text, nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    provincia = db.Column(db.String(100), nullable=False)
    inauguracion = db.Column(db.Integer, nullable=False)
    visible = db.Column(db.Boolean, default=True)
    punto = db.Column(Geometry(geometry_type="POINT", srid=4326), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    estado_conservacion = db.Column(db.String(50), nullable=False)

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

    eliminated_at = db.Column(db.DateTime, nullable=True)

    @property
    def latitud(self):
        if self.punto is None:
            return None
        return to_shape(self.punto).y

    @property
    def longitud(self):
        if self.punto is None:
            return None
        return to_shape(self.punto).x

    @property
    def cover_url(self):
       """
        Retorna la URL de la imagen de portada (is_cover=True) si existe.
       """
       cover = next((img for img in self.images if getattr(img, "is_cover", False)), None)
       return cover.url if cover else None

    tags = db.relationship(
        "Tag",
        secondary=site_tags,
        back_populates="sites",
        lazy="select",
    )

    history = db.relationship(
        "SiteHistory", backref="site", lazy="dynamic", cascade="all, delete"
    )

    images = db.relationship(
        "Image",
        back_populates="site",
        cascade="all, delete-orphan",
        lazy="select"
    )

    def __repr__(self):
        return f"<Sitio {self.nombre}>"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion_breve": self.descripcion_breve,
            "descripcion_completa": self.descripcion_completa,
            "ciudad": self.ciudad,
            "provincia": self.provincia,
            "inauguracion": self.inauguracion,
            "visible": self.visible,
            "latitud": self.latitud,
            "longitud": self.longitud,
            "categoria": self.categoria,
            "estado_conservacion": self.estado_conservacion,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "eliminated_at": self.eliminated_at.isoformat() if self.eliminated_at else None,
            "tags": [tag.name for tag in self.tags],
        }
