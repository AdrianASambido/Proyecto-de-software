"""
    Este controlador maneja las rutas relacionadas con las operaciones de usuarios
"""

from flask import Blueprint
from flask import render_template, request, redirect, url_for
from src.core import board_usuarios

bp = Blueprint("users", __name__, url_prefix=("/usuarios"))

@bp.get("/lista_usuarios")
def index():
    usuarios = board_usuarios.list_users()
    return render_template("usuarios/tabla_usuarios.html", users=usuarios), 200

@bp.get("/nuevo_usuario")
def add_form():
    return render_template("usuarios/agregar_usuario.html"), 200

@bp.post("/agregar_usuario")
def add_user():
    if request.method=="POST":
        user_data = dict(request.form)
        board_usuarios.add_user(user_data)
        return redirect(url_for("users.index"))
    
    return render_template("usuarios/agregar_usuario.html"), 200
