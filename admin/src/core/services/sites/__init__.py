"""
Este modelo representa las operaciones relacionadas con los sitios historicos.
"""

from src.core.database import db
from src.core.Entities.site import Site
from src.core.Entities.site_history import HistoryAction

from src.core.services.history import add_site_history
from datetime import datetime, timezone
from sqlalchemy import or_, and_
from geoalchemy2.shape import to_shape
from geoalchemy2.elements import WKTElement
from sqlalchemy import desc, asc
from src.core.services.tags import get_tag_by_id
from src.core.Entities.tag import Tag
from sqlalchemy.orm import joinedload

import csv
from io import StringIO

def list_sites(filtros: dict, page: int = 1, per_page: int = 3):
    """
    Retorna un objeto de paginación con los sitios históricos aplicando filtros y orden.
    """
    query = filter_sites(filtros)
    query = order_sites(query, filtros)
    return query.paginate(page=page, per_page=per_page, error_out=False)




def order_sites(query, filtros):
    """
    ordena los sitios
    """
    orden = filtros.get("order", "fecha_desc")
    opciones_orden = {
        "fecha_asc": Site.created_at.asc(),
        "fecha_desc": Site.created_at.desc(),
        "nombre_asc": Site.nombre.asc(),
        "nombre_desc": Site.nombre.desc(),
        "ciudad_asc": Site.ciudad.asc(),
        "ciudad_desc": Site.ciudad.desc(),
    }
    return query.order_by(opciones_orden.get(orden, Site.created_at.desc()))



def filter_sites(filtros):
    """
    filtra los sitios
    """
    query = Site.query.filter(Site.eliminated_at.is_(None))

    # Texto de búsqueda
    busqueda = filtros.get("busqueda")
    if busqueda:
        query = query.filter(
            or_(
                Site.nombre.ilike(f"%{busqueda}%"),
                Site.descripcion_breve.ilike(f"%{busqueda}%"),
            )
        )

    # Ciudad (texto )
    ciudad = filtros.get("ciudad")
    if ciudad:
        query = query.filter(Site.ciudad.ilike(f"%{ciudad}%"))

    # Provincia (exacta)
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

    # Visibilidad
    visible = filtros.get("visible")
    if visible in ("on", "1", True):
        query = query.filter(Site.visible.is_(True))

    # Tags (ids)
    tags_ids = filtros.get("tags")
    if tags_ids:
        tags_ids = [int(t) for t in tags_ids if str(t).isdigit()]
        if tags_ids:
            query = query.join(Tag, Site.tags).filter(Tag.id.in_(tags_ids)).distinct()

    return query

def get_site(site_id):
    """
    Retorna un sitio historico por su ID.
    """
    sitio = Site.query.get(site_id)
    if(sitio):
        return sitio
    else:
        return None


def modify_site(site_id, site_data):
    """
    Modifica un sitio historico existente.
    """
    sitio = Site.query.get(site_id)
    if not sitio:
        return None

    # tomar un snapshot dict de los valores originales ANTES de actualizar
    campos_site = Site.__table__.columns
    original_snapshot = {
        campo.name: getattr(sitio, campo.name, None) for campo in campos_site
    }

    if "visible" in site_data:
        sitio.visible = True if site_data["visible"] == "on" else False

    sitio.nombre = site_data.get("nombre", sitio.nombre)
    sitio.descripcion_breve = site_data.get(
        "descripcion_breve", sitio.descripcion_breve
    )
    sitio.descripcion_completa = site_data.get(
        "descripcion_completa", sitio.descripcion_completa
    )
    sitio.ciudad = site_data.get("ciudad", sitio.ciudad)
    sitio.provincia = site_data.get("provincia", sitio.provincia)
    sitio.inauguracion = site_data.get("inauguracion", sitio.inauguracion)
    lat = site_data.get("latitud")
    lng = site_data.get("longitud")
    if lat and lng:
        sitio.punto = WKTElement(f"POINT({lng} {lat})", srid=4326)

    sitio.categoria = site_data.get("categoria", sitio.categoria)
    sitio.estado_conservacion = site_data.get(
        "estado_conservacion", sitio.estado_conservacion
    )

    db.session.commit()


    # aca agregar a la tabla de historial
    add_site_history(
        site_id,
        HistoryAction.EDITAR,
        1,
        sitio,
        original_snapshot,
        list(site_data.keys()),
    )

    tags_viejas = [t.nombre for t in sitio.tags]  # relación many-to-many
    tags_nuevas = site_data.get("tags")
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


def add_site(site_data):
    """
    Agrega un nuevo sitio historico.
    """
    visible_value = site_data.get("visible")
    visible = True if visible_value == "on" else False

    lat = site_data.get("latitud")
    lng = site_data.get("longitud")

    if not lat or not lng:
        raise ValueError("Latitud y longitud son obligatorias")

    punto = WKTElement(f"POINT({lng} {lat})", srid=4326)

    nuevo_sitio = Site(
        nombre=site_data.get("nombre"),
        descripcion_breve=site_data.get("descripcion_breve"),
        descripcion_completa=site_data.get("descripcion_completa"),
        ciudad=site_data.get("ciudad"),
        provincia=site_data.get("provincia"),
        inauguracion=site_data.get("inauguracion"),
        punto=punto,
        categoria=site_data.get("categoria"),
        estado_conservacion=site_data.get("estado_conservacion"),
        visible=visible,
    )

    tags_data = site_data.get("tags", [])
    for tag_id in tags_data:
        tag = get_tag_by_id(tag_id)
        if tag is None:
            raise ValueError(f"Tag '{tag_id}' no encontrado")
        nuevo_sitio.tags.append(tag)

    db.session.add(nuevo_sitio)
    db.session.commit()

    add_site_history(
        nuevo_sitio.id, HistoryAction.CREAR, 1, site_data, None, list(site_data.keys())
    )

    return nuevo_sitio

def delete_site(site_id):
    """
    borra un sitio
    """
    sitio = Site.query.get(site_id)
    if not sitio:
        return False

    # snapshot antes de "eliminar"
    campos_site = Site.__table__.columns
    original_snapshot = {
        campo.name: getattr(sitio, campo.name, None) for campo in campos_site
    }

    # marcamos como eliminado (eliminación lógica)
    sitio.eliminated_at = datetime.now(timezone.utc)
    db.session.add(sitio)

        # Agregar ubicación como un solo campo
    if sitio.latitud is not None and sitio.longitud is not None:
        original_snapshot["ubicacion"] = {
            "latitud": sitio.latitud,
            "longitud": sitio.longitud
        }

    # Capturar tags si existen (cuando la relación esté activa)
    # if hasattr(sitio, 'tags') and sitio.tags:
    #     original_snapshot["tags"] = [tag.id for tag in sitio.tags]


    # guardamos historial
    add_site_history(
        site_id=sitio.id,
        accion=HistoryAction.ELIMINAR,
        usuario_modificador_id=1,
        sitio_cambiado=None,  # 🔹 porque estamos borrando
        sitio_original=original_snapshot,  # 🔹 snapshot antes del borrado
        campos_modificados=list(original_snapshot.keys()),
    )

    db.session.commit()
    return True

def export_sites_csv(filtros: dict = None):
    """
    Exporta la lista de sitios históricos en formato CSV.
    Aplica los mismos filtros que list_sites.
    """

    query = filter_sites(filtros if filtros else {})
    query = order_sites(query, filtros if filtros else {})


    output = StringIO()
    writer = csv.writer(output)

    # Escribir encabezados
    writer.writerow([
        "ID", "Nombre", "Descripción Breve", "Ciudad", "Provincia", 
        "Latitud", "Longitud", "Estado de Conservación", "Fecha de registro", "Tags"
    ])

    for sitio in query.all():
        punto_shape = to_shape(sitio.punto) if sitio.punto else None
        latitud = punto_shape.y if punto_shape else None
        longitud = punto_shape.x if punto_shape else None

        writer.writerow([
            sitio.id, sitio.nombre,
            sitio.descripcion_breve,
            sitio.ciudad,
            sitio.provincia,
            latitud,
            longitud,
            sitio.estado_conservacion,
            sitio.created_at,
            ";".join([tag.name for tag in sitio.tags])
        ])

    output.seek(0)
    return output.getvalue()

def get_current_timestamp_str():
    """
    Retorna la fecha y hora actual en formato YYYYMMDD_HHMM para usar en nombres de archivo.
    """
    return datetime.now().strftime("%Y%m%d_%H%M")