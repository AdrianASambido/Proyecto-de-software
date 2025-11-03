from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, BooleanField, SelectField, DecimalField, SubmitField, SelectMultipleField
from wtforms import FileField
from flask_wtf.file import FileAllowed, FileSize, MultipleFileField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, ValidationError


def validate_images(form, field):
    files = field.data or []
    if len(files) > 10:
        raise ValidationError("Máximo 10 imágenes.")

    allowed_ext = {"jpg", "png", "webp"}
    max_bytes = 5 * 1024 * 1024  # 5 MB

    for file in files:
        if not file or not getattr(file, "filename", None):
            raise ValidationError("Archivo inválido.")
        name = file.filename.lower()
        if "." not in name or name.rsplit(".", 1)[1] not in allowed_ext:
            raise ValidationError("Formato no permitido. Solo JPG, PNG o WEBP.")

        # Intentar determinar tamaño de forma segura
        size = getattr(file, "content_length", None)
        if not size:
            try:
                pos = file.stream.tell()
                file.stream.seek(0, 2)  # EOF
                size = file.stream.tell()
                file.stream.seek(pos)
            except Exception:
                size = None
        if size is not None and size > max_bytes:
            raise ValidationError("Cada imagen debe pesar como máximo 5 MB.")

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
            validate_images,
        ],
        render_kw={"multiple": True}
    )
    submit = SubmitField("Guardar")
