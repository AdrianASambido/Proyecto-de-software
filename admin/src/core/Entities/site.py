from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Site(db.Model):
    """
    Modelo que representa un sitio historico en la base de datos
    """

    __tablename__ = "sites"
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(100), nullable=False) 
    descripcionBreve=db.Column(db.Text, nullable=True)
    descripcionCompleta=db.Column(db.Text, nullable=True)
    ciudad=db.Column(db.String(100), nullable=False)
    provincia=db.Column(db.String(100), nullable=False)
    inauguracion=db.Column(db.Date, nullable=True)
    fecha_registro=db.Column(db.DateTime, nullable=False, default=db.func.now())
    visible=db.Column(db.Boolean, default=True)
    latitud=db.Column(db.Float, nullable=True)
    longitud=db.Column(db.Float, nullable=True)
    categoria=db.Column(db.String(50), nullable=True)
    estado_conservacion=db.Column(db.String(50), nullable=True)


    def __repr__(self):
        return f"<Sitio {self.nombre}>"
    

