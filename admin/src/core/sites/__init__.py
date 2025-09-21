"""
    Este modelo representa las operaciones relacionadas con los sitios historicos.
"""
from src.core.database import db
from src.core.Entities.site import Site
from datetime import datetime

def list_sites():
    """
    Retorna una lista de todos los sitios historicos.
    """
    sites=Site.query.all()
    return sites

def get_site(site_id):
    """
    Retorna un sitio historico por su ID.
    """
    sitio = Site.query.get(site_id)
    return sitio

def modify_site(site_id, site_data):
    """
    Modifica un sitio historico existente.
    """
    sitio = Site.query.get(site_id)
    if not sitio:
        return None
    visible_value = site_data.get("visible")  
    visible = True if visible_value == "on" else False

    sitio.nombre = site_data.get("nombre", sitio.nombre)
    sitio.descripcion_breve = site_data.get("descripcion_breve", sitio.descripcion_breve)
    sitio.descripcion_completa = site_data.get("descripcion_completa", sitio.descripcion_completa)
    sitio.ciudad = site_data.get("ciudad", sitio.ciudad)
    sitio.provincia = site_data.get("provincia", sitio.provincia)
    sitio.inauguracion = site_data.get("inauguracion", sitio.inauguracion)
    sitio.latitud = site_data.get("latitud", sitio.latitud)
    sitio.longitud = site_data.get("longitud", sitio.longitud)
    sitio.categoria = site_data.get("categoria", sitio.categoria)
    sitio.estado_conservacion = site_data.get("estado_conservacion", sitio.estado_conservacion)
    sitio.visible = visible

    db.session.commit()
    return sitio

def add_site(site_data):
    """
    Agrega un nuevo sitio historico.
    """
    visible_value = site_data.get("visible")  
    visible = True if visible_value == "on" else False
    nuevo_sitio = Site(
        nombre=site_data.get("nombre"),
        descripcion_breve=site_data.get("descripcion_breve"),
        descripcion_completa=site_data.get("descripcion_completa"),
        ciudad=site_data.get("ciudad"),
        provincia=site_data.get("provincia"),
        inauguracion=site_data.get("inauguracion"),
        latitud=site_data.get("latitud"),
        longitud=site_data.get("longitud"),
        categoria=site_data.get("categoria"),
        estado_conservacion=site_data.get("estado_conservacion"),
        visible=visible
    )

    db.session.add(nuevo_sitio)
    db.session.commit()
    return nuevo_sitio