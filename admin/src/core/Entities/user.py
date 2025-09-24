import enum
from src.core.database import db
from sqlalchemy import Enum
from datetime import datetime, timezone

class User(db.Model):
    """Modelo que representa un usuario en la base de datos"""

    __tablename__ = "users"
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(100), unique=True, nullable=False)
    nombre=db.Column(db.String(100), nullable=False)
    apellido=db.Column(db.String(100), nullable=False)
    contraseña_cifrada=db.Column(db.String(128), nullable=False)
    is_system_admin=db.Column(db.Boolean, default=False)
    activo=db.Column(db.Boolean, default=True)
    rol_id=db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    created_at=db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at=db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    role=db.relationship("Role", backpopulates="users")

    def __repr__(self):
        return f"<User {self.username}>"