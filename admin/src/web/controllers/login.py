from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash, session
from src.core.services import users as board_usuarios
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import OperationalError
from src.core.services.feature_flags import is_admin_maintenance_mode, get_admin_maintenance_message
bp = Blueprint("login", __name__, url_prefix=("/auth"))
bcrypt = Bcrypt()

@bp.get("/")
def login():
    if "user_id" in session:

        return redirect(url_for("home"))
    return render_template("login/login_usuario.html"), 200

@bp.get("/logout")
def logout():
    if(session.get("user_id")):
        session.pop("user_id", None)
        session.clear()
    else:
        flash("No hay una sesión activa.", "error")

    return redirect(url_for("login.login"))

@bp.post("/authenticate")
def authenticate():
   
    params = request.form
    email = params.get("email")
    password = params.get("password")
    
    try:
        user = board_usuarios.get_user_by_email(email)
    except OperationalError:
        flash("Problema con la conexión a la base de datos. Intente nuevamente.", "error")
        return redirect(url_for("login.login"))

    # Validar credenciales primero (evita llamar métodos sobre None)
    if not user or not bcrypt.check_password_hash(user.contraseña_cifrada, password):
        flash("Credenciales inválidas. Por favor, intente de nuevo.", "error")
        return redirect(url_for("login.login"))

    # Luego, chequeo de mantenimiento (ahora es seguro usar el user)
    if is_admin_maintenance_mode() and not user.is_system_admin_user():
        return render_template(
            "errores/maintenance.html",
            message=get_admin_maintenance_message(),
            title="Sistema en Mantenimiento"
        ), 503

    if user.eliminado:
        flash("No puede acceder. Esta cuenta está eliminada", "error")
        return redirect(url_for("login.login"))

    if not user.activo:
        flash("El usuario no está activo. Contacte al administrador.", "error")
        return redirect(url_for("login.login"))
    
    session["user_id"] = user.id
    session["username"] = user.nombre + " " + user.apellido if user.nombre and user.apellido else user.username
    session.permanent = True
    flash("Inicio de sesión exitoso.", "success")
    return redirect(url_for("home"))