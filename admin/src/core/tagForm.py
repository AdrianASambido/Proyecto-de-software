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
        Length(min=3, max=50, message="El nombre debe tener entre 3 y 50 caracteres."),
    ],  
        render_kw={"placeholder": "Ingresa el nombre de la etiqueta"}
    )
    submit = SubmitField("Guardar")
            