from src.core.database import db
from datetime import datetime, timezone


class Permission(db.Model):
    """
    Modelo que representa un permiso en la base de datos
    Sigue el patrón modulo_accion (ej: user_index, user_new, user_update, etc.)
    """

    __tablename__ = "permissions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    module = db.Column(db.String(50), nullable=False)  # modulo (ej: user, site, tag)
    action = db.Column(db.String(50), nullable=False)  # accion (ej: index, new, update, destroy, show)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    # Relación many-to-many con roles
    roles = db.relationship("Role", secondary="role_permissions", back_populates="permissions")
    
    def __repr__(self):
        return f"<Permission {self.name}>"
    
    @property
    def full_name(self):
        """Retorna el nombre completo del permiso en formato modulo_accion"""
        return f"{self.module}_{self.action}"
