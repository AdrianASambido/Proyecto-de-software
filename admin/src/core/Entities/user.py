import enum
from src.core.database import db
from sqlalchemy import Enum
from datetime import datetime, timezone


class rolEnum(enum.Enum):
    PUBLICO = "Usuario Público"
    EDITOR = "Editor"
    ADMINISTRADOR = "Administrador"


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
    bloqueado=db.Column(db.Boolean, default=False)  # Nuevo campo para bloqueo
    rol_id=db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    created_at=db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at=db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    role=db.relationship("Role", back_populates="users")

    __table_args__ = {'extend_existing': True}

    def __repr__(self):
        return f"<User {self.email}>"
    
    @property
    def is_admin(self):
        """Verifica si el usuario es administrador"""
        return self.role and self.role.name == "Administrador"
    
    @property
    def is_editor(self):
        """Verifica si el usuario es editor"""
        return self.role and self.role.name == "Editor"
    
    def can_login(self):
        """Verifica si el usuario puede iniciar sesión (activo y no bloqueado)"""
        return self.activo and not self.bloqueado
    
    def can_be_blocked(self):
        """Verifica si el usuario puede ser bloqueado (no es administrador)"""
        return not self.is_admin
    
    def has_permission(self, permission_name):
        """Verifica si el usuario tiene un permiso específico a través de su rol"""
        if not self.role:
            return False
        return self.role.has_permission(permission_name)
    
    def block(self):
        """Bloquea al usuario si es posible"""
        if self.can_be_blocked():
            self.bloqueado = True
            return True
        return False
    
    def unblock(self):
        """Desbloquea al usuario"""
        self.bloqueado = False
        return True
