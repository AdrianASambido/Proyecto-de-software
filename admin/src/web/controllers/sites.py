"""
    Este controlador maneja las rutas relacionadas con las operaciones de sitios históricos.
"""


from flask import Blueprint
from flask import render_template, request,redirect, url_for
from src.core import sites as board_sites


bp = Blueprint("sites", __name__, url_prefix=("/sitios"))

@bp.get("/")
def index():
    """
    Muestra la lista de sitios históricos.

    Renderiza la plantilla con la lista de sitios.
    """
    sitios=board_sites.list_sites()
    return render_template("sites/sites_table.html", sites=sitios), 200

@bp.route("/nuevo", methods=["GET", "POST"])
def add_site():
    """
    GET: muestra el formulario para crear un nuevo sitio.
    POST: procesa el formulario y crea el sitio.
    """
    if request.method == "POST":
        site_data = dict(request.form)
        board_sites.add_site(site_data)
        return redirect(url_for("sites.index"))
    
    return render_template("sites/add_site.html")


@bp.route("/modificar/<int:site_id>", methods=["GET", "POST"])
def modify(site_id):
    sitio = board_sites.get_site(site_id)
    if not sitio:
        return "Sitio no encontrado", 404

    if request.method == "POST":
        site_data = dict(request.form)
        board_sites.modify_site(site_id, site_data)
        return redirect(url_for("sites.index"))

    return render_template("sites/modify_site.html", site=sitio)

