"""
    Este modelo representa las operaciones relacionadas con los sitios historicos.
"""
from src.core.database import db
from src.core.Entities.site import Site
from datetime import datetime
from src.core.sites_history import add_site_history
from src.core.Entities.site_history import HistoryAction

def list_sites():
    """[c.name for c in
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

    add_site_history(
        nuevo_sitio.id,
        HistoryAction.CREAR,
        1,
        site_data,  
        None,
        list(site_data.keys())
    )

    return nuevo_sitio

def update_site(site_id, site_data):

    sitio_original = db.session.query(Site).filter_by(id=site_id).first()
    if sitio_original is None:
        return None

    # tomar un snapshot dict de los valores originales ANTES de actualizar
    campos_site = Site.__table__.columns
    original_snapshot = {campo.name: getattr(sitio_original, campo.name, None) for campo in campos_site}

    db.session.query(Site).filter_by(id=site_id).update(site_data)
    db.session.commit()    
    
    # aca agregar a la tabla de historial
    add_site_history(
        site_id, 
        HistoryAction.EDITAR, 
        1, 
        site_data,           
        original_snapshot,  
        list(site_data.keys())
    )