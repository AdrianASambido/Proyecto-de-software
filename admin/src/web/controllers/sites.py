"""
    Este controlador maneja las rutas relacionadas con las operaciones de sitios históricos.
"""

from flask import Blueprint
from flask import render_template, request,redirect, url_for
<<<<<<< HEAD
<<<<<<< HEAD
from src.core import sites as board_sites
=======

from src.core.services.sites import list_sites, add_site, get_site, modify_site
>>>>>>> dev
=======
<<<<<<< admin/src/web/controllers/sites.py

from src.core.services.sites import list_sites, add_site, get_site, modify_site
=======
from src.core import sites as board_sites
>>>>>>> admin/src/web/controllers/sites.py
>>>>>>> e2679686250ece3c02cada26eaf4e63eabe7eafd
import pycountry

bp = Blueprint("sites", __name__, url_prefix=("/sitios"))

provincias_arg=[sub.name for sub in pycountry.subdivisions.get(country_code="AR")]
@bp.get("/")
def index():
    """
    Muestra la lista de sitios históricos.

    Renderiza la plantilla con la lista de sitios.
    """

    filtros=request.args.to_dict()
<<<<<<< HEAD
<<<<<<< HEAD
    sitios = board_sites.list_sites(filtros).all()  # <-- ejecuta la query y devuelve lista
=======
    sitios = list_sites(filtros).all()  # <-- ejecuta la query y devuelve lista
>>>>>>> dev
=======

    sitios = list_sites(filtros).all()  # <-- ejecuta la query y devuelve lista

    sitios = board_sites.list_sites(filtros).all()  # <-- ejecuta la query y devuelve lista

>>>>>>> e2679686250ece3c02cada26eaf4e63eabe7eafd
    return render_template("sites/sites_table.html", items=sitios, provincias=provincias_arg)

@bp.route("/nuevo", methods=["GET", "POST"])
def add_site():
    """
    GET: muestra el formulario para crear un nuevo sitio.
    POST: procesa el formulario y crea el sitio.
    """
    if request.method == "POST":
        site_data = dict(request.form)
<<<<<<< HEAD
<<<<<<< HEAD
        board_sites.add_site(site_data)
=======
        add_site(site_data)
>>>>>>> dev
=======

        add_site(site_data)

        board_sites.add_site(site_data)

>>>>>>> e2679686250ece3c02cada26eaf4e63eabe7eafd
        return redirect(url_for("sites.index"))
    provincias_opts = [{"value": prov, "label": prov} for prov in provincias_arg]
    return render_template("sites/add_site.html",provincias=provincias_opts)


@bp.route("/modificar/<int:site_id>", methods=["GET", "POST"])
def modify(site_id):
<<<<<<< HEAD
<<<<<<< HEAD
    sitio = board_sites.get_site(site_id)
=======
    sitio = get_site(site_id)
>>>>>>> dev
=======

    sitio = get_site(site_id)

    sitio = board_sites.get_site(site_id)

>>>>>>> e2679686250ece3c02cada26eaf4e63eabe7eafd
    if not sitio:
        return "Sitio no encontrado", 404

    if request.method == "POST":
        site_data = dict(request.form)
<<<<<<< HEAD
<<<<<<< HEAD
        board_sites.modify_site(site_id, site_data)
=======
        modify_site(site_id, site_data)
>>>>>>> dev
=======

        modify_site(site_id, site_data)

        board_sites.modify_site(site_id, site_data)

>>>>>>> e2679686250ece3c02cada26eaf4e63eabe7eafd
        return redirect(url_for("sites.index"))

    return render_template("sites/modify_site.html", site=sitio)

