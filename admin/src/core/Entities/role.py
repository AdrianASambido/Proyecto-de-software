from src.core.database import db
from datetime import datetime, timezone

class Role(db.Model):
    """
    Modelo que representa un rol en la base de datos
    """
    
    __tablename__ = "roles"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    users = db.relationship("User", back_populates="role", cascade="all, delete")
    
    def __repr__(self):
        return f"<Role {self.name}>"
