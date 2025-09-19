"""
    Este modelo representa las operaciones relacionadas con los sitios historicos.
"""
from src.core.database import db
from src.core.Entities.site import Site
from datetime import datetime
from src.core.sites_history import add_site_history
from src.core.Entities.site_history import HistoryAction

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

    # aca agregar a la tabla de historial
    add_site_history(nuevo_sitio.id, HistoryAction.CREAR, 1, nuevo_sitio)

    return nuevo_sitio