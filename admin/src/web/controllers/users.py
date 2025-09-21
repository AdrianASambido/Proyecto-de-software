"""
    Este controlador maneja las rutas relacionadas con las operaciones de usuarios
"""

from flask import Blueprint
from flask import render_template, request, redirect, url_for

bp = Blueprint("users", __name__, url_prefix=("/usuarios"))

@bp.get("/")
def index():
    return render_template("usuarios/tabla_usuarios.html"), 200