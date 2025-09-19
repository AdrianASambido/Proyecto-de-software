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

def add_site(site_data):
    """
    Agrega un nuevo sitio historico.
    """
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
        visible=site_data.get("visible", True),
    )

    db.session.add(nuevo_sitio)
    db.session.commit()
    return nuevo_sitio