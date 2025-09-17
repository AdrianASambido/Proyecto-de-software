from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class SiteHistory(db.Model):
    """
    Modelo que representa el historial de modificaciones de un sitio a lo largo del tiempo
    """

    __tablename__ = "sites_history"
    id=db.Column(db.Integer, primary_key=True)
    sitio_id=db.Column(db.Integer, nullable=False)
    usuario_modificador_id=db.Column(db.Integer, nullable=False)
    fecha_modificacion=db.Column(db.DateTime, nullable=False, default=datetime.datetime.now()) 
    accion=db.Column(db.Enum("crear", "editar", "eliminar", "cambiar_tags", "cambiar_imagenes"), nullable=False) #crear, editar, eliminar, cambiar tags o imágenes
    # array de objetos con la siguiente estructura:
    # {
    #     "campo": "nombre del campo",
    #     "valor_anterior": "valor anterior", 
    #     "valor_nuevo": "valor nuevo"
    # }
    cambios=db.Column(db.JSON, nullable=True)
    

    def __repr__(self):
        return f"<Historial de modificacion {self.id}>"
    

