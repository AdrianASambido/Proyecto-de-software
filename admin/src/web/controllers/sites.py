"""
Este controlador maneja las rutas relacionadas con las operaciones de sitios históricos.
Este controlador maneja las rutas relacionadas con las operaciones de sitios históricos.
"""

from flask import Blueprint
from flask import render_template, request, redirect, url_for


from src.core.services import sites as board_sites
from src.core.services import tags as board_tags

from src.core.services.sites import list_sites, add_site, get_site, modify_site
from src.core.services.tags import list_tags
from flask import flash
import pycountry
from flask import current_app as app
from src.core.auth import login_required
bp = Blueprint("sites", __name__, url_prefix="/sitios")

provincias_arg = [sub.name for sub in pycountry.subdivisions.get(country_code="AR")]


@bp.get("/")
@login_required
def index():
    """
    Muestra la lista de sitios históricos.

    Renderiza la plantilla con la lista de sitios.
    """
    page = request.args.get("page", 1, type=int)
    per_page = 3

    filtros = request.args.to_dict()
    filtros.pop("page", None)
    filtros.pop("per_page", None)

    pagination = board_sites.list_sites(filtros).paginate(page=page, per_page=per_page)
    tags = [{"id": tag.id, "nombre": tag.name} for tag in board_tags.list_tags()]
    return render_template(
        "sites/sites_table.html",
        items=pagination.items,
        provincias=provincias_arg,
        pagination=pagination,
        filtros=filtros,
        tags=tags,
    )


@bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def add_site():
    """
    GET: muestra el formulario para crear un nuevo sitio.
    POST: procesa el formulario y crea el sitio.
    GET: muestra el formulario para crear un nuevo sitio.
    POST: procesa el formulario y crea el sitio.
    """
    if request.method == "POST":
        site_data = dict(request.form)
        board_sites.add_site(site_data)
        flash("Sitio histórico creado exitosamente.", "success")
        return redirect(url_for("sites.index"))
    tags = [{"value": tag.id, "label": tag.name} for tag in board_tags.list_tags()]

    provincias_opts = [{"value": prov, "label": prov} for prov in provincias_arg]
    return render_template("sites/add_site.html", provincias=provincias_opts, tags=tags)


@bp.route("/modificar/<int:site_id>", methods=["GET", "POST"])
@login_required
def modify(site_id):
    """
    GET: muestra el formulario para modificar un sitio histórico.
    POST: procesa el formulario y actualiza el sitio.
    """
    sitio = board_sites.get_site(site_id)

    if not sitio:
        return render_template("404.html"), 404

    if request.method == "POST":
        site_data = dict(request.form)

        board_sites.modify_site(site_id, site_data)
        flash("Sitio histórico modificado exitosamente.", "success")
        return redirect(url_for("sites.index"))
    tags = [{"value": tag.id, "label": tag.name} for tag in board_tags.list_tags()]

    provincias_opts = [{"value": prov, "label": prov} for prov in provincias_arg]
    return render_template(
        "sites/modify_site.html", site=sitio, provincias=provincias_opts, tags=tags
    )


@bp.post("/eliminar/<int:site_id>")
@login_required
def delete(site_id):
    """
    Elimina un sitio histórico.
    """

    sitio = board_sites.get_site(site_id)

    if not sitio:
        return render_template("404.html"), 404

    board_sites.delete_site(site_id)
    flash("Sitio histórico eliminado exitosamente.", "success")
    return redirect(url_for("sites.index"))

@bp.get("/exportar")
@login_required
def export():
    """
    Exporta la lista de sitios históricos en formato CSV.
    """
    filtros = request.form.to_dict()
    filtros.pop("exportar", None)

    csv_data = board_sites.export_sites_csv(filtros if len(filtros.keys()) > 0 else None)

    response = app.response_class(
        response=csv_data,
        status=200,
        mimetype="text/csv",
    )
    response.headers.set(
        "Content-Disposition",
        "attachment",
        filename=f"sitios_{board_sites.get_current_timestamp_str()}.csv",
    )

    return response


@bp.route("/<int:sitio_id>")
@login_required
def detail(sitio_id):
    sitio = board_sites.get_site(sitio_id)
    return render_template("sites/detail.html", sitio=sitio)
