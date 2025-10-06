from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from src.core.Entities import User
from flask_bcrypt import Bcrypt

class RegistrationForm(FlaskForm):
    nombre = StringField('Nombre real del Usuario', validators=[DataRequired(), Length(min=2, max=50)])
    apellido = StringField('Apellido del Usuario', validators=[DataRequired(), Length(min=2, max=50)])
    username = StringField('Nombre de usuario', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    contraseña = PasswordField('Contraseña', validators=[DataRequired()])
    rol_id = SelectField('Rol', choices=[('', 'Ninguno'), ('1', 'Administrador'), ('2', 'Editor')])
    submit = SubmitField('Guardar Usuario')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('El email ya está registrado en la base de datos. Por favor, elija otro.')
        
    def validate_email_format(self, email):
        if "@" not in email.data and "." not in email.data:
            raise ValidationError('El formato del email es inválido.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('No existe una cuenta con ese email. Contacte a nuestro administrador para registrarlo.')

    def validate_password(self, password):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not Bcrypt().check_password_hash(user.password, password.data):
            raise ValidationError('Contraseña incorrecta. Inténtelo de nuevo.')
        
class EditUserForm(FlaskForm):
    nombre = StringField('Nombre real del Usuario', validators=[DataRequired(), Length(min=2, max=50)])
    apellido = StringField('Apellido del Usuario', validators=[DataRequired(), Length(min=2, max=50)])
    username = StringField('Nombre de usuario', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    rol_id = SelectField('Rol', choices=[('', 'Ninguno'), ('1', 'Administrador'), ('2', 'Editor')])
    submit = SubmitField('Actualizar Usuario')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('El email ya está registrado en la base de datos. Por favor, elija otro.')