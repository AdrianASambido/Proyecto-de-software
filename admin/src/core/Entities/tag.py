from datetime import datetime, timezone
from src.core.database import db

# Tabla intermedia para muchos-a-muchos
site_tags = db.Table(
    "site_tags",
    db.Column("site_id", db.Integer, db.ForeignKey("sites.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    slug = db.Column(db.String(50), nullable=False, unique=True)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    deleted_at = db.Column(db.DateTime, nullable=True)

    # Relación muchos-a-muchos con sites
    sites = db.relationship(
        "Site",  # name del modelo de sites
        secondary=site_tags,
        #backref="tags",
        back_populates="tags"
    )

    def __repr__(self):
        return f"<Tag {self.name}>"
