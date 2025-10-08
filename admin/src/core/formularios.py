from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from src.core.Entities import User
from flask_bcrypt import Bcrypt

class RegistrationForm(FlaskForm):
    nombre = StringField('Nombre real del Usuario', validators=[DataRequired(), Length(min=2, max=50)])
    apellido = StringField('Apellido del Usuario', validators=[DataRequired(), Length(min=2, max=50)])
    username = StringField('Nombre de usuario', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired()])
    contraseña = PasswordField('Contraseña', validators=[DataRequired()])
    rol = SelectMultipleField('Rol', choices=[(1, 'Editor'), (2, 'Administrador')], validators=[DataRequired()], coerce=int)
    submit = SubmitField('Guardar Usuario')

    def validate_email(self, email):
        email_validar = Email(message="Formato inválido")
        try:
            email_validar(self, email)
        except ValidationError as e:
            raise ValidationError(str(e))

        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('El email ya está registrado en la base de datos. Por favor, elija otro.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

    def validate_email_password(self, email, password):
        email_validar = Email(message="Formato inválido")
        try:
            email_validar(self, email)
        except ValidationError as e:
            raise ValidationError(str(e))

        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('No existe una cuenta con ese email. Contacte a nuestro administrador para registrarlo.')
        
        if user and not user.is_active:
            raise ValidationError('La cuenta asociada a este email está inactiva. Contacte a nuestro administrador.')
        
        if user and user.eliminado:
            raise ValidationError('La cuenta asociada a este email ha sido eliminada. Contacte a nuestro administrador.')
        
        if user and not Bcrypt().check_password_hash(user.password, password.data):
            raise ValidationError('Contraseña incorrecta. Inténtelo de nuevo.')
        
class EditUserForm(FlaskForm):
    nombre = StringField('Nombre real del Usuario', validators=[Length(min=2, max=50)])
    apellido = StringField('Apellido del Usuario', validators=[Length(min=2, max=50)])
    username = StringField('Nombre de usuario', validators=[Length(min=2, max=20)])
    email = StringField('Email')
    contraseña = PasswordField('Contraseña', validators=[Length(min=6)])
    submit = SubmitField('Actualizar Usuario')

    def __init__(self, original_email, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_email = original_email

    #Verificar que el mail nuevo no esté en uso por otro usuario, ignorando el suyo si no se modificó
    def validate_email(self, email):
        email_validar = Email(message="Formato inválido")
        try:
            email_validar(self, email)
        except ValidationError as e:
            raise ValidationError(str(e))
        
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('El email ya está registrado en la base de datos. Por favor, elija otro.')

class EditUserAdminForm(FlaskForm):
    nombre = StringField('Nombre real del Usuario', validators=[Length(min=2, max=50)])
    apellido = StringField('Apellido del Usuario', validators=[Length(min=2, max=50)])
    username = StringField('Nombre de usuario', validators=[Length(min=2, max=20)])
    email = StringField('Email')
    rol_id = SelectMultipleField('Rol', choices=[(1, 'Editor'), (2, 'Administrador')], coerce=int)
    is_active = BooleanField('Activo', default=True)
    submit = SubmitField('Actualizar Usuario')

    def __init__(self, original_email, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_email(self, email):
        email_validar = Email(message="Formato inválido")
        try:
            email_validar(self, email)
        except ValidationError as e:
            raise ValidationError(str(e))

        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('El email ya está registrado en la base de datos. Por favor, elija otro.')