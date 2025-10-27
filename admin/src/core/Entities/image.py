from src.core.database import db
from datetime import datetime, timezone

class Image(db.Model):
    """
    Representa las imágenes de los sitios en la base de datos
    """

    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    order = db.Column(db.Integer, nullable=True)
    is_cover = db.Column(db.Boolean, default=False)


    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

   
    site_id = db.Column(db.Integer, db.ForeignKey("sites.id"), nullable=True)
    site = db.relationship("Site", back_populates="images")

    def __repr__(self):
        return f"<Image {self.id} - {self.title}>"
