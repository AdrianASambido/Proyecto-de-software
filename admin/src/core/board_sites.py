"""
    Este modelo representa las operaciones relacionadas con los sitios historicos.
"""
from core.Entities.site import Site,db

sites= [
    {
        "id": 1,
        "nombre": "Chichen Itza",
        "descripcion_breve": "Ciudad maya antigua",
        "descripcion_completa": "Chichen Itza fue una gran ciudad precolombina...",
        "ciudad": "Yucatan",
        "provincia": "Yucatan",
        "inauguracion": None,
        "latitud": 20.6843,
        "longitud": -88.5678,
        "categoria": "Arqueológico",
        "estado_conservacion": "Bueno",
        "fecha_registro": None,
        "visible": True,
    }
]
def list_sites():
    """
    Retorna una lista de todos los sitios historicos.
    """
    #sites=Site.query.all() cuando exista la base de datos
    
    return sites

def add_site(site_data):
    """
    Agrega un nuevo sitio historico.
    """
    nuevo_sitio = {
        "id": 3,  
        "nombre": site_data.get("nombre"),
        "descripcion_breve": site_data.get("descripcion_breve"),
        "descripcion_completa": site_data.get("descripcion_completa"),
        "ciudad": site_data.get("ciudad"),
        "provincia": site_data.get("provincia"),
        "inauguracion": site_data.get("inauguracion"),
        "latitud": site_data.get("latitud"),
        "longitud": site_data.get("longitud"),
        "categoria": site_data.get("categoria"),
        "estado_conservacion": site_data.get("estado_conservacion"),
        "fecha_registro": site_data.get("fecha_registro"),
        "visible": site_data.get("visible", True),

    }
    #db.session.add(nuevo_sitio) cuando exista la base de datos
    #db.session.commit() cuando exista la base de datos
    sites.append(nuevo_sitio)
    return nuevo_sitio