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
        "fecha_modificacion": datetime.datetime.now(),
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
    Retorna una lista de todos los sitios historicos.
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