from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Tabla intermedia para muchos-a-muchos
sitio_tags = db.Table(
    "sitio_tags",
    db.Column("sitio_id", db.Integer, db.ForeignKey("sites.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True)
)

class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    slug = db.Column(db.String(50), nullable=False, unique=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relación muchos-a-muchos con sitios
    sitios = db.relationship(
        "Site",  # Nombre del modelo de sitios
        secondary=sitio_tags,
        back_populates="tags"
    )

    def __repr__(self):
        return f"<Tag {self.nombre}>"
