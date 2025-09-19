"""
    Este modelo representa las operaciones relacionadas con los sitios historicos.
"""
from src.core.Entities.site_history import SiteHistory, HistoryAction
from src.core.Entities.site import Site
from src.core.database import db
from datetime import datetime, timezone, date
import enum

def _serialize_value(val):
    """Convierte valores no serializables por JSON a tipos compatibles."""
    if isinstance(val, enum.Enum):
        return val.value
    if isinstance(val, (datetime, date)):
        return val.isoformat()
    return val

site_1_history= [
    {
        "id": 1,
        "sitio_id": 1,
        "usuario_modificador_id": 1,
        "fecha_modificacion": datetime.now(timezone.utc),
        "accion": "crear",  # crear, editar, eliminar, cambiar_tags, cambiar_imagenes
        "cambios": [
            {
                "campo": "nombre",
                "valor_anterior": None,
                "valor_nuevo": "Chicho itza"
            },
            {
                "campo": "descripcion",
                "valor_anterior": None,
                "valor_nuevo": "Sitio ubicado en........"
            }
            # ... más cambios
        ]
    },
    {
        "id": 2,
        "sitio_id": 1,
        "usuario_modificador_id": 2,
        "fecha_modificacion": datetime.now(timezone.utc),
        "accion": "editar",  # crear, editar, eliminar, cambiar_tags, cambiar_imagenes
        "cambios": [
            {
                "campo": "nombre",
                "valor_anterior": "Chicho itza",
                "valor_nuevo": "Chichen Itza"
            }
        ]
    }
]

usuario_1={
    "id": 1,
    "nombre": "Usuario 1",
    "apellido": "Apellido 1",
}

usuario_2={
    "id": 2,
    "nombre": "Usuario 2",
    "apellido": "Apellido 2",
}
sitio_1={
    "id": 1,
    "nombre": "Chichen Itza",
}
sitio_2={
    "id": 2,
    "nombre": "Machu Picchu",
}

def list_site_history(sitio_id):
    """
    Retorna una lista de todos los cambios de un sitio historico.
    """
    if (sitio_id != 1):
        return {
        "sitio": sitio_2,
        "historial": []
    }
    
    for cambios in site_1_history:
        if(cambios["usuario_modificador_id"] == 1):
            cambios["datos_usuario"] = usuario_1
        else:
            cambios["datos_usuario"] = usuario_2

    return {
        "sitio": sitio_1,
        "historial": site_1_history
    }

def add_site_history(site_id,accion,usuario_modificador_id, sitio_cambiado):
    """
    Agrega un nuevo cambio en el historial de un sitio.
    """
    # validar que se reciban los datos correctamente
    if (site_id is None or accion is None or usuario_modificador_id is None or sitio_cambiado is None):
        return None

    # calcular cambios realizados en el sitio
    cambios_realizados=[]

    # obtener sitio original desde la DB si no es creacion o eliminacion
    sitio_original = None
    if accion not in (HistoryAction.CREAR, HistoryAction.ELIMINAR):
        sitio_original = Site.query.get(site_id)

    # campos a considerar en el historial (excluimos claves y timestamps)
    campos_site = [c.name for c in Site.__table__.columns
                   if c.name not in ("id", "created_at", "updated_at")]

    #si no existe y es creacion del mismo
    if (sitio_original is None and accion == HistoryAction.CREAR):
        for campo in campos_site:
            cambios_realizados.append({
                "campo": campo,
                "valor_anterior": None,
                "valor_nuevo": _serialize_value(getattr(sitio_cambiado, campo, None))
            })

    # si es eliminacion
    if (sitio_original is None and accion == HistoryAction.ELIMINAR):
        for campo in campos_site:
            cambios_realizados.append({
                "campo": campo,
                "valor_anterior": _serialize_value(getattr(sitio_cambiado, campo, None)),
                "valor_nuevo": None
            })

    # si es modificacion
    if (sitio_original is not None and sitio_cambiado is not None):
        # iterar por los campos modificados y agregarlos de la siguiente manera
        for campo in campos_site:
            valor_anterior = getattr(sitio_original, campo, None)
            valor_nuevo = getattr(sitio_cambiado, campo, None)
            if valor_anterior != valor_nuevo:
                cambios_realizados.append({
                    "campo": campo,
                    "valor_anterior": _serialize_value(valor_anterior),
                    "valor_nuevo": _serialize_value(valor_nuevo)
                })

    if (len(cambios_realizados) == 0):
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