from flask_wtf import FlaskForm

# Nombre (obligatorio, único, 3–50 caracteres, case-insensitive)
# Slug (autogenerado desde el nombre, único, solo minúsculas y guiones)
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError
from src.core.Entities.tag import Tag
from src.core.database import db


class TagForm(FlaskForm):
    name = StringField("Nombre", validators=[
        DataRequired(message="El nombre es obligatorio."),
        Length(min=2, max=50, message="El nombre debe tener entre 2 y 50 caracteres."),
        Regexp(r'^[a-zA-Z0-9\s]+$', message="El nombre solo puede contener letras, números y espacios.")
    ])
    submit = SubmitField("Guardar")
    slug = StringField("Slug", validators=[
        DataRequired(message="El slug es obligatorio."),
        Regexp(r'^[a-z0-9-]+$', message="El slug solo puede contener letras minúsculas, números y guiones.")
    ])

    # def validate_nombre(self, nombre):
    #     # Aquí podrías agregar lógica para verificar si el nombre ya existe en la base de datos
    #     existing_tag = Tag.query.filter(
    #         db.func.lower(Tag.name) == nombre.data.lower()
    #     ).first() 
    #     if nombre.data.lower() in existing_tag_names:
    #         raise ValidationError("El nombre ya existe. Por favor, elija otro.")
            