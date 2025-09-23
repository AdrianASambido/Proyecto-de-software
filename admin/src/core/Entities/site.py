
from src.core.database import db
from datetime import datetime, timezone

class Site(db.Model):
    """
    Modelo que representa un sitio historico en la base de datos
    """

    __tablename__ = "sites"
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(100), nullable=False) 
    descripcion_breve=db.Column(db.Text, nullable=False)
    descripcion_completa=db.Column(db.Text, nullable=False)
    ciudad=db.Column(db.String(100), nullable=False)
    provincia=db.Column(db.String(100), nullable=False)
    inauguracion=db.Column(db.Integer, nullable=False)
    visible=db.Column(db.Boolean, default=True)
    latitud=db.Column(db.Float, nullable=False)
    longitud=db.Column(db.Float, nullable=False)
    categoria=db.Column(db.String(50), nullable=False)
    estado_conservacion=db.Column(db.String(50), nullable=False)
    created_at=db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at=db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))


    def __repr__(self):
        return f"<Sitio {self.nombre}>"
    

