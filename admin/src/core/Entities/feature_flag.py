from src.core.database import db
from datetime import datetime, timezone


class FeatureFlag(db.Model):
    """
    Modelo que representa un feature flag en la base de datos
    """

    __tablename__ = "feature_flags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    is_enabled = db.Column(db.Boolean, default=False, nullable=False)
    maintenance_message = db.Column(db.Text, nullable=True)
    last_modified_by = db.Column(db.String(100), nullable=True)
    last_modified_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f"<FeatureFlag {self.name}: {'ON' if self.is_enabled else 'OFF'}>"

    def to_dict(self):
        """Convierte el objeto a diccionario para facilitar el uso en templates"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "is_enabled": self.is_enabled,
            "maintenance_message": self.maintenance_message,
            "last_modified_by": self.last_modified_by,
            "last_modified_at": (
                self.last_modified_at.strftime("%Y-%m-%d %H:%M:%S")
                if self.last_modified_at
                else None
            ),
            "created_at": (
                self.created_at.strftime("%Y-%m-%d %H:%M:%S")
                if self.created_at
                else None
            ),
        }
