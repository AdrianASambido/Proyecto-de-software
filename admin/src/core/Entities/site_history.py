from datetime import datetime, timezone
from src.core.database import db
import enum

class HistoryAction(enum.Enum):
    CREAR = "crear"
    EDITAR = "editar"
    ELIMINAR = "eliminar"
    CAMBIAR_TAGS = "cambiar_tags"
    CAMBIAR_IMAGENES = "cambiar_imagenes"

class SiteHistory(db.Model):
    """
    Modelo que representa el historial de modificaciones de un sitio a lo largo del tiempo
    """

    __tablename__ = "sites_history"
    id=db.Column(db.Integer, primary_key=True)
    sitio_id=db.Column(db.Integer, db.ForeignKey("sites.id"), nullable=False)
    usuario_modificador_id=db.Column(db.Integer, nullable=False)
    fecha_modificacion=db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc)) 
    accion=db.Column(db.Enum(HistoryAction), nullable=False)
    # array de objetos con la siguiente estructura:
    # {
    #     "campo": "nombre del campo",
    #     "valor_anterior": "valor anterior", 
    #     "valor_nuevo": "valor nuevo"
    # }
    cambios=db.Column(db.JSON, nullable=True)
    created_at=db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at=db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    

    def __repr__(self):
        return f"<Historial de modificacion {self.id}>"
    