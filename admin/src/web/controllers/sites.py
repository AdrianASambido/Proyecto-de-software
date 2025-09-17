"""
    Este controlador maneja las rutas relacionadas con las operaciones de sitios históricos.
"""


from flask import Blueprint
from flask import render_template, request
from src.core import board_sites


bp = Blueprint("sites", __name__, url_prefix=("/sitios"))

@bp.get("/")
def index():
    """
    Muestra la lista de sitios históricos.

    Renderiza la plantilla con la lista de sitios.
    """
    sitios=board_sites.list_sites()
    return render_template("sites/sites_table.html", sites=sitios), 200

@bp.get("/nuevo")
def add_form():
    """
    Muestra el formulario para agregar un nuevo sitio histórico.
    """
    return render_template("sites/add_site.html"), 200

@bp.post("/add")
def add_site():
    """
    Procesa el formulario y agrega el sitio, luego redirige a la lista.
    """
    site_data = dict(request.form)
    board_sites.add_site(site_data)
    return render_template("sites_table.html", sites=board_sites.list_sites()), 200