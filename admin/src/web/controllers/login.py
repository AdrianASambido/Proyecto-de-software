from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash, session
from src.core import board_usuarios

bp = Blueprint("login", __name__, url_prefix=("/auth"))

@bp.get("/")
def login():
    if "user" in session:
        flash("Ya has iniciado sesión.", "warning")
        return redirect(url_for("home"))
    return render_template("login/login_usuario.html"), 200

@bp.get("/logout")
def logout():
    session.clear()
    flash("La sesion se cerró", "success")
    return redirect(url_for("login.login"))

@bp.post("/authenticate")
def authenticate():
    params = request.form
    user = board_usuarios.buscar_usuario(params.get("email"), params.get("password"))
    if not user:
        flash("Credenciales inválidas. Por favor, intente de nuevo.", "error")
        return redirect(url_for("login.login"))
    
    session["user"] = user.email
    flash("Inicio de sesión exitoso.", "success")
    return render_template("home.html"), 200