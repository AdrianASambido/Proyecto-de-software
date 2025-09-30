"""
Este modelo representa las operaciones relacionadas con los sitios historicos.
"""

from src.core.Entities.site_history import SiteHistory, HistoryAction
from src.core.Entities.site import Site
from src.core.database import db
from datetime import datetime, timezone, date
import enum
from geoalchemy2.shape import to_shape
from geoalchemy2 import WKTElement
from shapely.geometry import mapping
from geoalchemy2.elements import WKBElement

def _serialize_value(val):
    """Convierte valores no serializables por JSON a tipos compatibles."""
    if isinstance(val, enum.Enum):
        return val.value
    if isinstance(val, (datetime, date)):
        return val.isoformat()
    if isinstance(val, (WKTElement,WKBElement)):
        geom = to_shape(val)   
        return mapping(geom)  
    return val


# helper para obtener valores desde dict u objeto
def _get_field(obj, campo):
    if obj is None:
        return None
    if isinstance(obj, dict):
        return obj.get(campo)
    return getattr(obj, campo, None)


usuario_1 = {
    "id": 1,
    "nombre": "Usuario 1",
    "apellido": "Apellido 1",
}

per_page = 2


def list_site_history(sitio_id, page: int = 1, filtros: dict | None = None):
    """
    Retorna una lista de todos los cambios de un sitio historico.
    """

    sitio = db.session.query(Site).filter_by(id=sitio_id).first()

    if sitio is None:
        return None

    query_filters = db.session.query(SiteHistory).filter_by(sitio_id=sitio_id)
    print(filtros)
    if filtros is not None:
        # por usuario
        if filtros.get("usuario") is not None:
            query_filters = query_filters.filter_by(
                usuario_modificador_id=filtros.get("usuario")
            )
        # por tipo de acción
        if filtros.get("accion") is not None:
            accion_value = filtros.get("accion")
            accion_enum = next((a for a in HistoryAction if a.value == accion_value), None)
            if accion_enum:
                query_filters = query_filters.filter_by(accion=accion_enum)
        # por rango de fechas
        if filtros.get("fecha_desde") is not None:
            query_filters = query_filters.filter(
                SiteHistory.fecha_modificacion >= filtros.get("fecha_desde")
            )
        if filtros.get("fecha_hasta") is not None:
            query_filters = query_filters.filter(
                SiteHistory.fecha_modificacion <= filtros.get("fecha_hasta")
            )

    # Asumiendo que tienes definida esta variable con la cantidad por página
    per_page = 20  

    offset = (int(page) - 1) * per_page

    paginated_query = (
        query_filters.order_by(SiteHistory.fecha_modificacion.desc())
        .limit(per_page + 1)
        .offset(offset)
    )
    site_history = paginated_query.all()

    has_more = len(site_history) > per_page

    for cambios in site_history:
        cambios.datos_usuario = usuario_1  # Esto lo tienes que definir o modificar según contexto

    return {
        "sitio": sitio,
        "historial": site_history[:-1] if has_more else site_history,
        "has_more": has_more,
        "page": page,
    }

def add_site_history(
    site_id,
    accion,
    usuario_modificador_id,
    sitio_cambiado,
    sitio_original=None,
    campos_modificados=None,
):
    """
    Agrega un nuevo cambio en el historial de un sitio.
    """
    # validar que se reciban los datos correctamente
    if site_id is None or accion is None or usuario_modificador_id is None:
        return None
    # Para eliminar permitimos sitio_cambiado = None pero requerimos sitio_original
    if accion == HistoryAction.ELIMINAR and sitio_original is None:
        return None
    # Para crear requerimos sitio_cambiado
    if accion == HistoryAction.CREAR and sitio_cambiado is None:
        return None
    # Para editar requerimos ambos
    if accion == HistoryAction.EDITAR and (
        sitio_cambiado is None or sitio_original is None
    ):
        return None

    # calcular cambios realizados en el sitio
    cambios_realizados = []

    # si no se especifican campos modificados, usar todos (excepto id/created_at/updated_at)
    if campos_modificados is None:
        campos_modificados = [
            c.name
            for c in Site.__table__.columns
            if c.name not in ("id", "created_at", "updated_at")
        ]

    # si no existe y es creacion del mismo
    if sitio_original is None and accion == HistoryAction.CREAR:
        for campo in campos_modificados:
            nuevo = _get_field(sitio_cambiado, campo)
            # solo registrar campos provistos/no nulos para creacion
            if nuevo is not None:
                cambios_realizados.append(
                    {
                        "campo": campo,
                        "valor_anterior": None,
                        "valor_nuevo": _serialize_value(nuevo),
                    }
                )

    # si es eliminacion
    if sitio_original is not None and accion == HistoryAction.ELIMINAR:
        for campo in campos_modificados:
            viejo = _get_field(sitio_original, campo)
            if viejo is not None:
                cambios_realizados.append(
                    {
                        "campo": campo,
                        "valor_anterior": _serialize_value(viejo),
                        "valor_nuevo": None,
                    }
                )

    # si es modificacion
    if sitio_original is not None and sitio_cambiado is not None:
        # iterar por los campos modificados y agregarlos de la siguiente manera
        for campo in campos_modificados:
            valor_anterior = _get_field(sitio_original, campo)
            valor_nuevo = _get_field(sitio_cambiado, campo)
            if valor_anterior != valor_nuevo:
                cambios_realizados.append(
                    {
                        "campo": campo,
                        "valor_anterior": _serialize_value(valor_anterior),
                        "valor_nuevo": _serialize_value(valor_nuevo),
                    }
                )

    if len(cambios_realizados) == 0:
        return None

    nueva_entrada = SiteHistory(
        sitio_id=site_id,
        usuario_modificador_id=usuario_modificador_id,
        fecha_modificacion=datetime.now(timezone.utc),
        accion=accion,
        cambios=cambios_realizados,
    )

    # insertar en la base de datos
    db.session.add(nueva_entrada)
    db.session.commit()
    return nueva_entrada
