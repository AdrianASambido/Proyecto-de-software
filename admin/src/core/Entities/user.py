from src.core.database import db
from datetime import datetime, timezone


class rolEnum(enum.Enum):
    PUBLICO = "Usuario Público"
    EDITOR = "Editor"
    ADMINISTRADOR = "Administrador"


class User(db.Model):
    """Modelo que representa un usuario en la base de datos"""

    __tablename__ = "users"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    email=db.Column(db.String(100), unique=True, nullable=False)
    nombre=db.Column(db.String(100), nullable=False)
    username=db.Column(db.String(50), unique=True, nullable=False)
    apellido=db.Column(db.String(100), nullable=False)
    contraseña_cifrada=db.Column(db.String(128), nullable=False)
    is_system_admin=db.Column(db.Boolean, default=False)
    activo=db.Column(db.Boolean, default=True)
    created_at=db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at=db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    eliminado=db.Column(db.Boolean, default=False)
    bloqueado=db.Column(db.Boolean, default=False)

    roles=db.relationship("Role", secondary="user_roles", back_populates="users")

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
