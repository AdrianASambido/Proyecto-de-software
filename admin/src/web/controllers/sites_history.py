"""
Este controlador maneja las rutas relacionadas con el historial de sitios.
"""

from flask import Blueprint
from flask import render_template, request
from flask import abort

from src.core.services.history import list_site_history
from src.core.Entities.site_history import HistoryAction
from src.core.auth import login_required
bp = Blueprint("sites_history", __name__, url_prefix=("/historial/<int:sitio_id>"))



@bp.get("/")
@login_required
def index(sitio_id):
    """
    Muestra la lista de sitios históricos.

    Renderiza la plantilla con la lista de sitios.
    """

    page = request.args.get("page", default=1, type=int)
    order = request.args.get("order", default="asc", type=str)
    filtros = {}
    if (
        request.args.get("usuario") is not None
        and request.args.get("usuario") != ""
        and request.args.get("usuario") != "Todos"
    ):
        filtros["usuario"] = request.args.get("usuario")
    if (
        request.args.get("accion") is not None
        and request.args.get("accion") != ""
        and request.args.get("accion") != "Todos"
    ):
        filtros["accion"] = request.args.get("accion")
    if (
        request.args.get("fecha_desde") is not None
        and request.args.get("fecha_desde") != ""
    ):
        filtros["fecha_desde"] = request.args.get("fecha_desde")
    if (
        request.args.get("fecha_hasta") is not None
        and request.args.get("fecha_hasta") != ""
    ):
        filtros["fecha_hasta"] = request.args.get("fecha_hasta")


    datos_historial = list_site_history(
        sitio_id, page, order, filtros if len(filtros.keys()) > 0 else None
    )

    if datos_historial is None:
        return abort(404)

    # obtener usuarios para crear bien el selector 
    usuarios_options = []
    for cambio in datos_historial["historial"]:
        if cambio.datos_usuario not in usuarios_options:
            usuarios_options.append(
                {"value": cambio.datos_usuario["id"], "label": 
                f"{cambio.datos_usuario['nombre']} {cambio.datos_usuario['apellido']}"}
            )

    print(datos_historial)

    return (
        render_template(
            "site_history/changes_list.html",
            lista_de_cambios=datos_historial["historial"],
            sitio=datos_historial["sitio"],
            
            # datos para filtros
            active_filters_count=len(filtros),
            HistoryAction=HistoryAction,
            usuarios_options=usuarios_options,
            # filtros
            filtros=filtros,

            # datos para paginacion
            pagination=datos_historial["pagination"],

            # ordenamiento
            order=order,
            orders=[{"value": "asc", "label": "Ascendente"}, {"value": "desc", "label": "Descendente"}],
        ),
        200,
    )
