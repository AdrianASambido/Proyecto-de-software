"""
Este controlador maneja las rutas relacionadas con las operaciones de sitios históricos.
Este controlador maneja las rutas relacionadas con las operaciones de sitios históricos.
"""

from flask import Blueprint
from flask import render_template, request, redirect, url_for


from src.core.services import sites as board_sites
from src.core.services import tags as board_tags
from flask import session
from src.core.services.sites import list_sites, add_site, get_site, modify_site
from src.core.services.tags import list_tags
from flask import flash
from src.core.siteForm import SiteForm
import pycountry
from flask import current_app as app
from src.core.auth import login_required,permission_required,admin_required
bp = Blueprint("sites", __name__, url_prefix="/sitios")

provincias_arg = [sub.name for sub in pycountry.subdivisions.get(country_code="AR")]



@bp.get("/")
@permission_required('site_index')
@login_required
def index():
    """
    Muestra la lista de sitios históricos.
    """
    page = request.args.get("page", 1, type=int)
    per_page = 25

    filtros = request.args.to_dict()
    filtros.pop("page", None)
    filtros.pop("per_page", None)

    # Ya devuelve un objeto paginado
    pagination = board_sites.list_sites(filtros, page=page, per_page=per_page)

    tags = [{"value": tag.id, "label": tag.name} for tag in board_tags.list_tags()]

    #el filtro de provincias necesita las provincias en formato {'value': 'Buenos Aires', 'label': 'Buenos Aires'}
    provincias_arg = [
    {"value": sub.name, "label": sub.name}
    for sub in pycountry.subdivisions.get(country_code="AR")
]

    return render_template(
        "sites/sites_table.html",
        items=pagination.items,
        provincias=provincias_arg,
        pagination=pagination,
        filtros=filtros,
        tags=tags,
    )



@bp.route("/nuevo", methods=["GET", "POST"])
@permission_required("site_new")
@login_required
def add_site():
    """
    GET: muestra el formulario para crear un nuevo sitio histórico.
    POST: procesa el formulario y crea el sitio.
    """
    siteForm = SiteForm()

    # Provincias
    provincias_opts = [(prov, prov) for prov in provincias_arg]
    siteForm.provincia.choices = provincias_opts

    # Tags
    tags = [(tag.id, tag.name) for tag in board_tags.list_tags()]
    siteForm.tags.choices = tags

  
    if siteForm.tags.data is None:
        siteForm.tags.data = []

    # Procesar POST
    if siteForm.validate_on_submit():
        site_data = {
            "nombre": siteForm.nombre.data,
            "descripcion_breve": siteForm.descripcion_breve.data,
            "descripcion_completa": siteForm.descripcion_completa.data,
            "ciudad": siteForm.ciudad.data,
            "provincia": siteForm.provincia.data,
            "inauguracion": siteForm.inauguracion.data,
            "visible": siteForm.visible.data,
            "categoria": siteForm.categoria.data,
            "estado_conservacion": siteForm.estado_conservacion.data,
            "latitud": float(siteForm.latitud.data) if siteForm.latitud.data else None,
            "longitud": float(siteForm.longitud.data) if siteForm.longitud.data else None,
            "tags": siteForm.tags.data,
        }
<<<<<<< HEAD
        user_id=session.get("user_id")
        board_sites.add_site(site_data,user_id)
=======

        board_sites.add_site(site_data)
>>>>>>> 3622861 (fix:detalles en sitios/tags)
        flash("Sitio histórico creado exitosamente.", "success")
        return redirect(url_for("sites.index"))

    # Renderizar formulario
    return render_template(
        "sites/add_site.html",
        form=siteForm,
        provincias=provincias_opts,
        tags=tags
    )


@bp.route("/modificar/<int:site_id>", methods=["GET", "POST"])
@permission_required('site_update')
@login_required
def modify(site_id):
    """
    GET: muestra el formulario para modificar un sitio histórico.
    POST: procesa el formulario y actualiza el sitio.
    """
    site = board_sites.get_site(site_id)
    form = SiteForm(obj=site)
    form.provincia.choices = [(p, p) for p in provincias_arg]
    form.tags.choices = [(t.id, t.name) for t in board_tags.list_tags()]
   
  
    form.tags.data = [t.id for t in site.tags] 
    if form.validate_on_submit():
        user_id=session.get("user_id")
        board_sites.modify_site(site_id, form.data,user_id)
        flash("Sitio actualizado correctamente.", "success")
        return redirect(url_for("sites.index"))

    return render_template("sites/modify_site.html", form=form)


@bp.post("/eliminar/<int:site_id>")
@login_required
@permission_required('site_destroy')
def delete(site_id):
    """
    Elimina un sitio histórico.
    """

    sitio = board_sites.get_site(site_id)

    if not sitio:
        return render_template("404.html"), 404
    user_id=session.get("user_id")
    board_sites.delete_site(site_id,user_id)
    flash("Sitio histórico eliminado exitosamente.", "success")
    return redirect(url_for("sites.index"))

@bp.get("/exportar")
@login_required
@permission_required('site_export')
def export():
    """
    Exporta la lista de sitios históricos en formato CSV.
    """
    filtros = request.args.to_dict()
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
@permission_required('site_show')
@login_required
def detail(sitio_id):
    """
    renderiza los detalles del sitio
    """
    sitio = board_sites.get_site(sitio_id)
    return render_template("sites/detail.html", sitio=sitio)
