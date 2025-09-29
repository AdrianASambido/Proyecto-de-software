from src.core.database import db
from datetime import datetime, timezone


# Tabla de asociación many-to-many entre roles y permisos
role_permissions = db.Table(
    'role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
)


class Role(db.Model):
    """
    Modelo que representa un rol en la base de datos
    """

    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    users = db.relationship("User", back_populates="role")
    permissions = db.relationship("Permission", secondary=role_permissions, back_populates="roles")
    
    def __repr__(self):
        return f"<Role {self.name}>"
    
    def has_permission(self, permission_name):
        """Verifica si el rol tiene un permiso específico"""
        return any(perm.name == permission_name for perm in self.permissions)
    
    def add_permission(self, permission):
        """Agrega un permiso al rol"""
        if permission not in self.permissions:
            self.permissions.append(permission)
    
    def remove_permission(self, permission):
        """Remueve un permiso del rol"""
        if permission in self.permissions:
            self.permissions.remove(permission)
