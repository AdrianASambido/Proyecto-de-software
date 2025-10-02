"""
Este modelo representa las operaciones relacionadas con los sitios historicos.
"""

from src.core.database import db
from src.core.Entities.site import Site
from src.core.Entities.site_history import HistoryAction

from src.core.services.history import add_site_history
from datetime import datetime
from sqlalchemy import or_, and_


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

    busqueda = filtros.get("busqueda")
    if busqueda:
        query = query.filter(
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


def modify_site(site_id, site_data, tags_nuevas=None):
    """
    Modifica un sitio historico existente.

    Args:
        site_id: ID del sitio a modificar
        site_data: Datos del formulario
        tags_nuevas: Lista opcional de IDs de tags nuevas (cuando la relación esté activa)
    """
    sitio = Site.query.get(site_id)
    if not sitio:
        return None

    # tomar un snapshot dict de los valores originales ANTES de actualizar
    campos_site = Site.__table__.columns
    original_snapshot = {
        campo.name: getattr(sitio, campo.name, None) for campo in campos_site
    }

    # Capturar tags viejas si existen (cuando la relación esté activa)
    tags_viejas = []
    if hasattr(sitio, 'tags') and sitio.tags:
        tags_viejas = [tag.id for tag in sitio.tags]

    visible_value = site_data.get("visible")
    visible = True if visible_value == "on" else False

    # Convertir tipos correctamente desde el formulario
    inauguracion = int(site_data.get("inauguracion")) if site_data.get("inauguracion") else sitio.inauguracion
    latitud = float(site_data.get("latitud")) if site_data.get("latitud") else sitio.latitud
    longitud = float(site_data.get("longitud")) if site_data.get("longitud") else sitio.longitud

    sitio.nombre = site_data.get("nombre", sitio.nombre)
    sitio.descripcion_breve = site_data.get(
        "descripcion_breve", sitio.descripcion_breve
    )
    sitio.descripcion_completa = site_data.get(
        "descripcion_completa", sitio.descripcion_completa
    )
    sitio.ciudad = site_data.get("ciudad", sitio.ciudad)
    sitio.provincia = site_data.get("provincia", sitio.provincia)
    sitio.inauguracion = inauguracion
    sitio.latitud = latitud
    sitio.longitud = longitud
    sitio.categoria = site_data.get("categoria", sitio.categoria)
    sitio.estado_conservacion = site_data.get(
        "estado_conservacion", sitio.estado_conservacion
    )
    sitio.visible = visible

    db.session.commit()

    # Crear snapshot de valores nuevos con tipos correctos
    new_snapshot = {
        "nombre": sitio.nombre,
        "descripcion_breve": sitio.descripcion_breve,
        "descripcion_completa": sitio.descripcion_completa,
        "ciudad": sitio.ciudad,
        "provincia": sitio.provincia,
        "inauguracion": sitio.inauguracion,
        "latitud": sitio.latitud,
        "longitud": sitio.longitud,
        "categoria": sitio.categoria,
        "estado_conservacion": sitio.estado_conservacion,
        "visible": sitio.visible,
    }

    # aca agregar a la tabla de historial
    add_site_history(
        site_id,
        HistoryAction.EDITAR,
        1,
        new_snapshot,
        original_snapshot,
        list(new_snapshot.keys()),
    )

    # Si cambiaron las tags, registrar en historial aparte
    if tags_nuevas is not None and sorted(tags_viejas) != sorted(tags_nuevas):
        add_site_history(
            site_id,
            HistoryAction.CAMBIAR_TAGS,
            1,
            {"tags": tags_nuevas},
            {"tags": tags_viejas},
            ["tags"],
        )

    return sitio


def add_site(site_data, tags_ids=None):
    """
    Agrega un nuevo sitio historico.

    Args:
        site_data: Datos del formulario
        tags_ids: Lista opcional de IDs de tags (cuando la relación esté activa)
    """
    visible_value = site_data.get("visible")
    visible = True if visible_value == "on" else False

    # Convertir tipos correctamente
    inauguracion = int(site_data.get("inauguracion")) if site_data.get("inauguracion") else None
    latitud = float(site_data.get("latitud")) if site_data.get("latitud") else None
    longitud = float(site_data.get("longitud")) if site_data.get("longitud") else None

    nuevo_sitio = Site(
        nombre=site_data.get("nombre"),
        descripcion_breve=site_data.get("descripcion_breve"),
        descripcion_completa=site_data.get("descripcion_completa"),
        ciudad=site_data.get("ciudad"),
        provincia=site_data.get("provincia"),
        inauguracion=inauguracion,
        latitud=latitud,
        longitud=longitud,
        categoria=site_data.get("categoria"),
        estado_conservacion=site_data.get("estado_conservacion"),
        visible=visible,
    )

    db.session.add(nuevo_sitio)
    db.session.commit()

    # Crear snapshot con tipos correctos para historial
    new_snapshot = {
        "nombre": nuevo_sitio.nombre,
        "descripcion_breve": nuevo_sitio.descripcion_breve,
        "descripcion_completa": nuevo_sitio.descripcion_completa,
        "ciudad": nuevo_sitio.ciudad,
        "provincia": nuevo_sitio.provincia,
        "inauguracion": nuevo_sitio.inauguracion,
        "categoria": nuevo_sitio.categoria,
        "estado_conservacion": nuevo_sitio.estado_conservacion,
        "visible": nuevo_sitio.visible,
    }

    # Agregar ubicación como un solo campo
    if latitud is not None and longitud is not None:
        new_snapshot["ubicacion"] = {
            "latitud": latitud,
            "longitud": longitud
        }

    # Agregar tags si existen
    if tags_ids is not None and len(tags_ids) > 0:
        new_snapshot["tags"] = tags_ids

    add_site_history(
        nuevo_sitio.id, HistoryAction.CREAR, 1, new_snapshot, None, list(new_snapshot.keys())
    )

    return nuevo_sitio

def delete_site(site_id):
    """
    Elimina un sitio historico.
    """
    sitio = Site.query.get(site_id)
    if not sitio:
        return False

    # tomar un snapshot dict de los valores originales ANTES de eliminar
    original_snapshot = {
        "nombre": sitio.nombre,
        "descripcion_breve": sitio.descripcion_breve,
        "descripcion_completa": sitio.descripcion_completa,
        "ciudad": sitio.ciudad,
        "provincia": sitio.provincia,
        "inauguracion": sitio.inauguracion,
        "categoria": sitio.categoria,
        "estado_conservacion": sitio.estado_conservacion,
        "visible": sitio.visible,
    }

    # Agregar ubicación como un solo campo
    if sitio.latitud is not None and sitio.longitud is not None:
        original_snapshot["ubicacion"] = {
            "latitud": sitio.latitud,
            "longitud": sitio.longitud
        }

    # Capturar tags si existen (cuando la relación esté activa)
    if hasattr(sitio, 'tags') and sitio.tags:
        original_snapshot["tags"] = [tag.id for tag in sitio.tags]

    db.session.delete(sitio)
    db.session.commit()

    add_site_history(
        site_id, HistoryAction.ELIMINAR, 1, None, original_snapshot, list(original_snapshot.keys())
    )

    return True