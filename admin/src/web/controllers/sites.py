"""
Este controlador maneja las rutas relacionadas con las operaciones de sitios históricos.
"""

from flask import Blueprint
from flask import render_template, request, redirect, url_for


from src.core.services import sites as board_sites


from src.core.services.sites import list_sites, add_site, get_site, modify_site

from flask import flash
import pycountry

bp = Blueprint("sites", __name__, url_prefix="/sitios")

provincias_arg = [sub.name for sub in pycountry.subdivisions.get(country_code="AR")]


@bp.get("/")
def index():
    """
    Muestra la lista de sitios históricos.

    Renderiza la plantilla con la lista de sitios.
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 3, type=int)

    filtros = request.args.to_dict()
    filtros.pop("page", None)       # 👈 eliminar si existe
    filtros.pop("per_page", None)   # 👈 eliminar si existe

    # devolvemos un objeto Pagination
    pagination = board_sites.list_sites(filtros).paginate(
        page=page, per_page=per_page
    )

    return render_template(
        "sites/sites_table.html",
        items=pagination.items,
        provincias=provincias_arg,
        pagination=pagination,
        filtros=filtros   # 👈 pasamos los filtros "limpios"
    )


@bp.route("/nuevo", methods=["GET", "POST"])
def add_site():
    """
    GET: muestra el formulario para crear un nuevo sitio.
    POST: procesa el formulario y crea el sitio.
    """
    if request.method == "POST":
        site_data = dict(request.form)
        board_sites.add_site(site_data)
        flash("Sitio histórico creado exitosamente.", "success")
        return redirect(url_for("sites.index"))

    provincias_opts = [{"value": prov, "label": prov} for prov in provincias_arg]
    return render_template("sites/add_site.html", provincias=provincias_opts)


@bp.route("/modificar/<int:site_id>", methods=["GET", "POST"])
def modify(site_id):

    sitio = board_sites.get_site(site_id)

    if not sitio:
        return "Sitio no encontrado", 404

    if request.method == "POST":
        site_data = dict(request.form)

        board_sites.modify_site(site_id, site_data)
        flash("Sitio histórico modificado exitosamente.", "success")
        return redirect(url_for("sites.index"))

    return render_template("sites/modify_site.html", site=sitio)

@bp.post("/eliminar/<int:site_id>")
def delete(site_id):
    """
    Elimina un sitio histórico.
    """
    sitio = board_sites.get_site(site_id)

    if not sitio:
        return "Sitio no encontrado", 404

    board_sites.delete_site(site_id)
    flash("Sitio histórico eliminado exitosamente.", "success")
    return redirect(url_for("sites.index"))
