"""
Este controlador maneja las rutas relacionadas con el historial de sitios.
"""

from flask import Blueprint
from flask import render_template, request
from flask import abort

from src.core.services.history import list_site_history
from src.core.Entities.site_history import HistoryAction

bp = Blueprint("sites_history", __name__, url_prefix=("/historial/<int:sitio_id>"))


@bp.get("/")
def index(sitio_id):
    """
    Muestra la lista de sitios históricos.

    Renderiza la plantilla con la lista de sitios.
    """

    page = request.args.get("page", default=1, type=int)
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
        sitio_id, page, filtros if len(filtros.keys()) > 0 else None
    )

    if datos_historial is None:
        return abort(404)

    usuarios_en_historial = []
    for cambio in datos_historial["historial"]:
        if cambio.datos_usuario not in usuarios_en_historial:
            usuarios_en_historial.append(cambio.datos_usuario)

    return (
        render_template(
            "site_history/changes_list.html",
            HistoryAction=HistoryAction,
            lista_de_cambios=datos_historial["historial"],
            sitio=datos_historial["sitio"],
            has_more=datos_historial["has_more"],
            page=datos_historial["page"],
            filtros=filtros,
            usuarios_en_historial=usuarios_en_historial,
        ),
        200,
    )
