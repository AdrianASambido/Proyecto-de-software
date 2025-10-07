from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash, session
from src.core.services import users as board_usuarios
from flask_bcrypt import Bcrypt

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
    
    user = board_usuarios.get_user_by_email(email)
    if not user or not bcrypt.check_password_hash(user.contraseña_cifrada, password):
        flash("Credenciales inválidas. Por favor, intente de nuevo.", "error")
        return redirect(url_for("login.login"))
    
    if user.eliminado:
        flash("No puede acceder. Esta cuenta está eliminada", "error")
        return redirect(url_for("login.login"))
    
    if not user.activo:
        flash("El usuario no está activo. Contacte al administrador.", "error")
        return redirect(url_for("login.login"))
    
    session["user_id"] = user.id
    session.permanent = True
    flash("Inicio de sesión exitoso.", "success")
    return redirect(url_for("home"))