import enum
from src.core.database import db
from sqlalchemy import Enum

class rolEnum(enum.Enum):
    PUBLICO="Usuario Público"
    EDITOR="Editor"
    ADMINISTRADOR="Administrador"

class User(db.Model):
    """Modelo que representa un usuario en la base de datos"""

    __tablename__ = "users"
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(100), unique=True, nullable=False)
    nombre=db.Column(db.String(100), nullable=False)
    apellido=db.Column(db.String(100), nullable=False)
    contraseña_hasheada=db.Column(db.String(128), nullable=False)
    is_admin=db.Column(db.Boolean, default=False)
    activo=db.Column(db.Boolean, default=True)
    rol=db.Column(Enum(rolEnum), db.String(50), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"