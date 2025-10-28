"""
Este modelo representa las operaciones relacionadas con los sitios historicos.
"""

from src.core.Entities.site_history import SiteHistory, HistoryAction
from src.core.Entities.site import Site
from src.core.Entities.tag import Tag
from src.core.Entities.user import User

from geoalchemy2.shape import to_shape
from geoalchemy2 import WKTElement
from shapely.geometry import mapping
from geoalchemy2.elements import WKBElement

import enum
from src.core.database import db
from datetime import datetime, timezone, date
from sqlalchemy.orm import AppenderQuery

def _serialize_value(val):
    """Convierte valores no serializables por JSON a tipos compatibles."""
    if isinstance(val, enum.Enum):
        return val.value
    if isinstance(val, (datetime, date)):
        return val.isoformat()
    if isinstance(val, (WKTElement, WKBElement)):
        geom = to_shape(val)
        return mapping(geom)
    if isinstance(val, AppenderQuery):
        # Convierte la relación dinámica en una lista de IDs o nombres
        return [v.id for v in val.all()]
    if isinstance(val, list):
        return [_serialize_value(v) for v in val]
    return val


# helper para obtener valores desde dict u objeto
def _get_field(obj, campo):
    if obj is None:
        return None
    if isinstance(obj, dict):
        return obj.get(campo)
    return getattr(obj, campo, None)

per_page = 25

def list_site_history(sitio_id, page: int = 1, order: str = "desc", filtros: dict | None = None):

    """
    Retorna una lista de todos los cambios de un sitio historico.
    """

    sitio = db.session.query(Site).filter_by(id=sitio_id).first()

    if sitio is None:
        return None

    # por usuario, por tipo de acción, por rango de fechas. JOIN con User y solo columnas necesarias
    stmt = (
         db.session.query(SiteHistory)
        .with_entities(
            SiteHistory,
            User
        )
        .join(User, User.id == SiteHistory.usuario_modificador_id)
        .filter(SiteHistory.sitio_id == sitio_id)
    )

    if filtros is not None:
        # por usuario
        if filtros.get("usuario") is not None:
            stmt = stmt.where(SiteHistory.usuario_modificador_id == filtros.get("usuario")) 
        # por tipo de acción
        if filtros.get("accion") is not None:
            stmt = stmt.where(
                SiteHistory.accion == HistoryAction(filtros.get("accion"))
            )
        # por rango de fechas
        if filtros.get("fecha_desde") is not None:
            stmt = stmt.where(
                SiteHistory.fecha_modificacion >= filtros.get("fecha_desde")
            )
        if filtros.get("fecha_hasta") is not None:
            stmt = stmt.where(
                SiteHistory.fecha_modificacion <= filtros.get("fecha_hasta")
            )

    pagination = db.paginate(
        stmt.order_by(
            SiteHistory.fecha_modificacion.desc() 
            if order == "desc" or order == "" 
            else SiteHistory.fecha_modificacion.asc()
        ),
        page=page,
        per_page=per_page,
        error_out=False,
    )

    site_history = []
    for hist in pagination.items:
        usuario = User.query.get(hist.usuario_modificador_id)
        hist.datos_usuario = {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
        }
        if hist.accion == HistoryAction.CAMBIAR_TAGS and hist.cambios:
            for c in hist.cambios:
                if isinstance(c, dict) and c.get("campo") == "tags":
                    ids_previos = c.get("valor_anterior") or []
                    ids_nuevos = c.get("valor_nuevo") or []
                    todos_ids = list({*ids_previos, *ids_nuevos})
                    if todos_ids:
                        tags = db.session.query(Tag).filter(Tag.id.in_(todos_ids)).all()
                        mapa = {t.id: {"id": t.id, "name": t.name} for t in tags}
                        c["valor_anterior_detalle"] = [mapa.get(tid) for tid in ids_previos if tid in mapa]
                        c["valor_nuevo_detalle"] = [mapa.get(tid) for tid in ids_nuevos if tid in mapa]
        site_history.append(hist)

    return {
        "sitio": sitio,
        "historial": site_history,
        "pagination": {
            "page": pagination.page,
            "pages": pagination.pages,
            "has_next": pagination.has_next,
            "next_num": pagination.next_num,
            "has_prev": pagination.has_prev,
            "prev_num": pagination.prev_num,
        }
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
        # Crear mensaje descriptivo para la creación
        nombre = _get_field(sitio_cambiado, "nombre") or "Sin nombre"
        categoria = _get_field(sitio_cambiado, "categoria") or "sin categoría"
        ciudad = _get_field(sitio_cambiado, "ciudad") or "ubicación desconocida"
        provincia = _get_field(sitio_cambiado, "provincia") or ""

        ubicacion = f"{ciudad}, {provincia}" if provincia else ciudad

        mensaje = f"Se creó el sitio '{nombre}', con categoría {categoria}, en {ubicacion}"

        cambios_realizados.append(
            {
                "campo": "datos",
                "valor_anterior": None,
                "valor_nuevo": mensaje,
            }
        )

    # si es eliminacion
    if sitio_original is not None and accion == HistoryAction.ELIMINAR:
        # Crear mensaje descriptivo para la eliminación
        nombre = _get_field(sitio_original, "nombre") or "Sin nombre"
        categoria = _get_field(sitio_original, "categoria") or "sin categoría"
        ciudad = _get_field(sitio_original, "ciudad") or "ubicación desconocida"
        provincia = _get_field(sitio_original, "provincia") or ""

        ubicacion = f"{ciudad}, {provincia}" if provincia else ciudad

        mensaje = f"Se eliminó el sitio '{nombre}', con categoría {categoria}, en {ubicacion}"

        cambios_realizados.append(
            {
                "campo": "datos",
                "valor_anterior": mensaje,
                "valor_nuevo": None,
            }
        )

    # si es modificacion
    if sitio_original is not None and sitio_cambiado is not None:

        # detectar cambios en coordenadas para agruparlos
        lat_cambio = False
        lng_cambio = False
        lat_vieja = None
        lat_nueva = None
        lng_vieja = None
        lng_nueva = None

        # iterar por los campos modificados y agregarlos de la siguiente manera
        for campo in campos_modificados:
            valor_anterior = _get_field(sitio_original, campo)
            valor_nuevo = _get_field(sitio_cambiado, campo)

            # Detectar cambios en coordenadas
            if campo == "latitud" and valor_anterior != valor_nuevo:
                lat_cambio = True
                lat_vieja = valor_anterior
                lat_nueva = valor_nuevo
            elif campo == "longitud" and valor_anterior != valor_nuevo:
                lng_cambio = True
                lng_vieja = valor_anterior
                lng_nueva = valor_nuevo
            elif campo not in ["latitud", "longitud"] and valor_anterior != valor_nuevo:
                cambios_realizados.append(
                    {
                        "campo": campo,
                        "valor_anterior": _serialize_value(valor_anterior),
                        "valor_nuevo": _serialize_value(valor_nuevo),
                    }
                )

        # Si cambió alguna coordenada, agregar como un solo cambio de "ubicacion"
        if lat_cambio or lng_cambio:
            # Obtener valores actuales si no cambiaron
            if not lat_cambio:
                lat_vieja = _get_field(sitio_original, "latitud")
                lat_nueva = _get_field(sitio_cambiado, "latitud")
            if not lng_cambio:
                lng_vieja = _get_field(sitio_original, "longitud")
                lng_nueva = _get_field(sitio_cambiado, "longitud")

            cambios_realizados.append(
                {
                    "campo": "ubicacion",
                    "valor_anterior": {
                        "latitud": _serialize_value(lat_vieja),
                        "longitud": _serialize_value(lng_vieja)
                    },
                    "valor_nuevo": {
                        "latitud": _serialize_value(lat_nueva),
                        "longitud": _serialize_value(lng_nueva)
                    },
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
