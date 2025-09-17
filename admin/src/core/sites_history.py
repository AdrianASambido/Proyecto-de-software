"""
    Este modelo representa las operaciones relacionadas con los sitios historicos.
"""
from core.Entities.site_history import SiteHistory,db
import datetime

site_1_history= [
    {
        "id": 1,
        "sitio_id": 1,
        "usuario_modificador_id": 1,
        "fecha_modificacion": datetime.datetime.now(),
        "accion": "editar",  # crear, editar, eliminar, cambiar_tags, cambiar_imagenes
        "cambios": [
            {
                "campo": "nombre_del_campo",
                "valor_anterior": "valor anterior",
                "valor_nuevo": "valor nuevo"
            }
            # ... más cambios
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
sitio={
    "id": 1,
    "nombre": "Chichen Itza",
}

def list_site_history(sitio_id):
    """
    Retorna una lista de todos los sitios historicos.
    """
    if (sitio_id != 1):
        return None
    
    for cambios in site_1_history:
        if(cambios["usuario_modificador_id"] == 1):
            cambios["datos_usuario"] = usuario_1
        else:
            cambios["datos_usuario"] = usuario_2

    return {
        "sitio": sitio,
        "historial": site_1_history
    }