"""
    Este controlador maneja las rutas relacionadas con el historial de sitios.
"""


from flask import Blueprint
from flask import render_template, request
from src.core.sites_history import list_site_history
from flask import abort
from src.core.Entities.site_history import HistoryAction

bp = Blueprint("site_history", __name__, url_prefix=("/historial/<int:sitio_id>"))

@bp.get("/")
def index(sitio_id):
    """
    Muestra la lista de sitios históricos.

    Renderiza la plantilla con la lista de sitios.
    """

    page = request.args.get("page", default=1, type=int)
    datos_historial=list_site_history(sitio_id, page, request.args.get("filtros", None))

    if (datos_historial is None):
        return abort(404)
        
    return render_template("site_history/changes_list.html", 
        HistoryAction=HistoryAction,
        lista_de_cambios=datos_historial["historial"], 
        sitio=datos_historial["sitio"],
        has_more=datos_historial["has_more"],
        page=datos_historial["page"]
    ), 200
