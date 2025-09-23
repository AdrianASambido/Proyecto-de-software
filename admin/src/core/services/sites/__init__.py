"""
    Este modelo representa las operaciones relacionadas con los sitios historicos.
"""
from src.core.database import db
from src.core.Entities.site import Site
from src.core.Entities.site_history import HistoryAction

from src.core.services.history import add_site_history
from datetime import datetime
from sqlalchemy import or_,and_


def list_sites(filtros: dict):
    """
    Retorna una lista de sitios históricos aplicando filtros dinámicos.
    Filtros soportados:
      - ciudad (texto o selector)
      - provincia (selector)
      - tags (lista)
      - estado_conservacion (Bueno | Regular | Malo)
      - fecha_desde / fecha_hasta
      - visible (checkbox)
    """
    query = Site.query

    busqueda= filtros.get("busqueda")
    if busqueda:
        query=query.filter(
            or_(
                Site.nombre.ilike(f"%{busqueda}%"),
                Site.descripcion_breve.ilike(f"%{busqueda}%"),
            
            )
        )
    # Ciudad (texto parcial o exacto)
    ciudad = filtros.get("ciudad")
    if ciudad:
        query = query.filter(Site.ciudad.ilike(f"%{ciudad}%"))

    # Provincia (igualdad)
    provincia = filtros.get("provincia")
    if provincia:
        query = query.filter(Site.provincia == provincia)

   
    # Estado de conservación
    estado = filtros.get("estado_conservacion")
    if estado:
        query = query.filter(Site.estado_conservacion == estado)

    # Rango de fechas
    fecha_desde = filtros.get("fecha_desde")
    if fecha_desde:
        query = query.filter(Site.created_at >= fecha_desde)

    fecha_hasta = filtros.get("fecha_hasta")
    if fecha_hasta:
        query = query.filter(Site.created_at <= fecha_hasta)

    # Visibilidad (checkbox → "on" o "1")
    visible = filtros.get("visible")
    if visible:
        query = query.filter(Site.visible == True)

    return query


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

    # tomar un snapshot dict de los valores originales ANTES de actualizar
    campos_site = Site.__table__.columns
    original_snapshot = {campo.name: getattr(sitio, campo.name, None) for campo in campos_site}
  
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

    # aca agregar a la tabla de historial
    add_site_history(
        site_id, 
        HistoryAction.EDITAR, 
        1, 
        site_data,           
        original_snapshot,  
        list(site_data.keys())
    )

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

    add_site_history(
        nuevo_sitio.id,
        HistoryAction.CREAR,
        1,
        site_data,  
        None,
        list(site_data.keys())
    )

    return nuevo_sitio