from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, BooleanField, SelectField, DecimalField, SubmitField, SelectMultipleField
from wtforms import FileField
from flask_wtf.file import FileAllowed, FileSize, MultipleFileField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class SiteForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=100)])
    descripcion_breve = TextAreaField("Descripción breve", validators=[DataRequired()])
    descripcion_completa = TextAreaField("Descripción completa", validators=[DataRequired()])
    ciudad = StringField("Ciudad", validators=[DataRequired(), Length(max=100)])
    provincia = SelectField("Provincia", validators=[DataRequired()], choices=[])
    inauguracion = IntegerField("Año de inauguración", validators=[DataRequired(), NumberRange(min=0, max=2025)])
    visible = BooleanField("Visible", default=True)
    categoria = StringField("Categoría", validators=[DataRequired(), Length(max=50)])
    estado_conservacion = SelectField("Estado de conservación", validators=[DataRequired()],
                                      choices=[("Bueno", "Bueno"), ("Regular", "Regular"), ("Malo", "Malo")])
    latitud = DecimalField("Latitud", places=6, validators=[DataRequired(message="Debe seleccionar una ubicación en el mapa")])
    longitud = DecimalField("Longitud", places=6, validators=[DataRequired(message="Debe seleccionar una ubicación en el mapa")])
    tags = SelectMultipleField("Tags", coerce=int)
    images = MultipleFileField(
        "Imágenes",
        validators=[
            Optional(),
            FileAllowed(["jpg", "png", "webp"], "Formato no permitido"),
            # FileSize puede no validar cada archivo en todas las versiones; validar tamaño en el controlador si es necesario
        ],
        render_kw={"multiple": True}
    )
    submit = SubmitField("Guardar")
