"""
    Este controlador maneja las rutas relacionadas con el historial de sitios.
"""


from flask import Blueprint
from flask import render_template, request
from src.core import sites_history
from flask import abort


bp = Blueprint("site_history", __name__, url_prefix=("/historial/<int:sitio_id>"))

@bp.get("/")
def index(sitio_id):
    """
    Muestra la lista de sitios históricos.

    Renderiza la plantilla con la lista de sitios.
    """
    # sitio=sites_history.get_site(sitio_id)
    datos_historial=sites_history.list_site_history(sitio_id)
    return render_template("site_history/changes_list.html", lista_de_cambios=datos_historial["historial"], sitio=datos_historial["sitio"]), 200
