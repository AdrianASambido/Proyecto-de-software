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
from sqlalchemy import desc, asc,func
from src.core.services.tags import get_tag_by_id
from src.core.Entities.tag import Tag
from sqlalchemy.orm import joinedload
from src.core.Entities.image import Image
from sqlalchemy.orm import aliased
import csv
from io import StringIO

def list_sites(filtros: dict, page: int = 1, per_page: int = 25, include_cover=False):
    """
    Retorna un objeto de paginación con los sitios históricos aplicando filtros y orden.
    """
    query = filter_sites(filtros)
    query = geoespatial_search(query, filtros)
    query = order_sites(query, filtros)

    if include_cover:
        Cover = aliased(Image)
        subquery = (
            db.session.query(Cover.site_id, Cover.url)
            .filter(Cover.is_cover == True)
            .subquery()
        )

        query = query.outerjoin(subquery, Site.id == subquery.c.site_id)
        pagination = query.add_columns(subquery.c.url.label("cover_url")).paginate(
            page=page, per_page=per_page, error_out=False
        )

        results = []
        for site, cover_url in pagination.items:
         
            site._cover_url = cover_url  
            results.append(site)

        pagination.items = results
        return pagination

    return query.paginate(page=page, per_page=per_page, error_out=False)


def geoespatial_search(query,filtros):
    """
    filtra los sitios dentro del radio dado usando postgis
    """

def geoespatial_search(query,filtros):
    """
    filtra los sitios dentro del radio dado usando postgis
    """

    lat=filtros.get("latitud")
    lon=filtros.get("longitud")
    rad=filtros.get("radio")
    if lat and lon and rad:
        lat=float(lat)
        lon=float(lon)
        rad=float(rad)

        query = query.filter(
            func.ST_DWithin(
                func.Geography(Site.punto),
                func.Geography(func.ST_MakePoint(lon, lat)),
                rad * 1000
            )
        )
    return query

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
    Filtra los sitios según los filtros proporcionados.
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

    # Ciudad
    ciudad = filtros.get("ciudad")
    if ciudad:
        query = query.filter(Site.ciudad.ilike(f"%{ciudad}%"))

    # Provincia
    provincia = filtros.get("provincia")
    if provincia:
        query = query.filter(Site.provincia == provincia)

    # Estado de conservación
    estado = filtros.get("estado_conservacion")
    if estado:
        query = query.filter(Site.estado_conservacion == estado)

    # Rango de fechas
    fecha_desde_str = filtros.get("fecha_desde")
    fecha_hasta_str = filtros.get("fecha_hasta")

    fecha_desde = None
    fecha_hasta = None

    if fecha_desde_str:
        try:
            fecha_desde = datetime.strptime(fecha_desde_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Fecha desde inválida: {fecha_desde_str}")

    if fecha_hasta_str:
        try:
            fecha_hasta = datetime.strptime(fecha_hasta_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Fecha hasta inválida: {fecha_hasta_str}")

    if fecha_desde and fecha_hasta:
        if fecha_desde > fecha_hasta:
            raise ValueError("El rango de fechas no es válido: desde mayor que hasta.")

    if fecha_desde:
        query = query.filter(Site.created_at >= fecha_desde)
    if fecha_hasta:
        query = query.filter(Site.created_at <= fecha_hasta)

    # Visibilidad
    visible = filtros.get("visible")
    if visible in ("on", "1", True,"Si"):
        query = query.filter(Site.visible.is_(True))
    elif visible in ("off",0,False,"No"):
        query= query.filter(Site.visible.is_(False))

    # Tags
    tags_ids = filtros.get("tags")
    if tags_ids:
        tags_ids = [int(t) for t in tags_ids if str(t).isdigit()]
        if tags_ids:
            query = query.join(Tag, Site.tags).filter(Tag.id.in_(tags_ids)).distinct()

    return query

def get_site(site_id, include_images=False):
    sitio = Site.query.get(site_id)
    if not sitio:
        return None

    if include_images:
        sitio.images_data = [
            {
                "id": img.id,
                "url": img.url,
                "title": img.title,
                "description": img.description,
                "order": img.order,
                "is_cover": img.is_cover,
            }
            for img in sitio.images
        ]
    return sitio



def modify_site(site_id, site_data, user_id):
    """
    Modifica un sitio histórico existente.
    """
   
    sitio = Site.query.get(site_id)
    if not sitio:
        return None

    # Snapshot de valores originales ANTES de actualizar
    campos_site = Site.__table__.columns
    original_snapshot = {
        campo.name: getattr(sitio, campo.name, None) for campo in campos_site
    }
    original_snapshot["latitud"] = sitio.latitud
    original_snapshot["longitud"] = sitio.longitud
    
    # Guardar las tags viejas antes de modificarlas
    tags_viejas = [t.id for t in sitio.tags]

    # Actualizar campos simples
    sitio.visible = site_data.get("visible", False)
    sitio.nombre = site_data.get("nombre", sitio.nombre)
    sitio.descripcion_breve = site_data.get("descripcion_breve", sitio.descripcion_breve)
    sitio.descripcion_completa = site_data.get("descripcion_completa", sitio.descripcion_completa)
    sitio.ciudad = site_data.get("ciudad", sitio.ciudad)
    sitio.provincia = site_data.get("provincia", sitio.provincia)
    sitio.inauguracion = site_data.get("inauguracion", sitio.inauguracion)
    sitio.categoria = site_data.get("categoria", sitio.categoria)
    sitio.estado_conservacion = site_data.get("estado_conservacion", sitio.estado_conservacion)

    # Coordenadas (si vienen)
    lat = site_data.get("latitud")
    lng = site_data.get("longitud")
    if lat and lng:
        sitio.punto = WKTElement(f"POINT({lng} {lat})", srid=4326)

    sitio.categoria = site_data.get("categoria", sitio.categoria)
    sitio.estado_conservacion = site_data.get(
        "estado_conservacion", sitio.estado_conservacion
    )
    # actualizar tags si vienen
    tags_data = site_data.get("tags", [])
    sitio.tags=[]
    for tag_id in tags_data:
        
        tag = get_tag_by_id(tag_id)
        if tag is None:
            raise ValueError(f"Tag '{tag_id}' no encontrado")
        sitio.tags.append(tag)
    db.session.commit()

    # Nuevo snapshot después de la modificación
    nuevo_snapshot = {
        campo.name: getattr(sitio, campo.name, None) for campo in campos_site
    }
    nuevo_snapshot["latitud"] = sitio.latitud
    nuevo_snapshot["longitud"] = sitio.longitud

    # Convertir booleanos a texto legible
    original_snapshot["visible"] = "Sí" if original_snapshot["visible"] else "No"
    nuevo_snapshot["visible"] = "Sí" if nuevo_snapshot["visible"] else "No"


    campos_modificados = list(site_data.keys())
    if (lat is not None) or (lng is not None):
        if "latitud" not in campos_modificados:
            campos_modificados.append("latitud")
        if "longitud" not in campos_modificados:
            campos_modificados.append("longitud")

    # Agregar registro general de modificación
    add_site_history(
        site_id,
        HistoryAction.EDITAR,
        user_id,
        nuevo_snapshot,
        original_snapshot,
        list(site_data.keys()),
    )

    # Comparar tags antes y después
    tags_nuevas = [t.id for t in sitio.tags]
    if sorted(tags_viejas) != sorted(tags_nuevas):
        add_site_history(
            site_id,
            HistoryAction.CAMBIAR_TAGS,
            user_id,
            {"tags": tags_nuevas},
            {"tags": tags_viejas},
            ["tags"],
        )

    return sitio


def add_site(site_data,user_id):
    """Agrega un nuevo sitio historico"""
    lat = site_data.get("latitud")
    lng = site_data.get("longitud")
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
        visible=site_data.get("visible",False),
    )

    tags_data = site_data.get("tags", [])
    for tag_id in tags_data:
        tag = get_tag_by_id(tag_id)
        if tag is None:
            raise ValueError(f"Tag '{tag_id}' no encontrado")
        nuevo_sitio.tags.append(tag)

    images_data = site_data.get("images", [])
    
    # crear las imagenes en la db y asociarlas
    for image_obj in images_data:
        nueva_imagen = Image(
            url=image_obj,
            title="",
            description="",
            is_cover=False
        )
        nuevo_sitio.images.append(nueva_imagen)

    db.session.add(nuevo_sitio)
    db.session.commit()

    #en el historial se muestra si  o no , no true o false
    visible=site_data.get("visible")
    historial_data = site_data.copy()
    historial_data["visible"] = "Sí" if visible else "No"
    add_site_history(
        nuevo_sitio.id, HistoryAction.CREAR, user_id, historial_data, None, list(site_data.keys())
    )
    return nuevo_sitio

def actualizar_historial(nuevo,accion,original=None):
    pass

def delete_site(site_id,user_id):
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

    # marco como eliminado (eliminación lógica)
    sitio.eliminated_at = datetime.now(timezone.utc)
    db.session.add(sitio)

    # Agregar ubicación 
    if sitio.latitud is not None and sitio.longitud is not None:
        original_snapshot["ubicacion"] = {
            "latitud": sitio.latitud,
            "longitud": sitio.longitud
        }

    add_site_history(
        site_id=sitio.id,
        accion=HistoryAction.ELIMINAR,
        usuario_modificador_id=user_id,
        sitio_cambiado=None, 
        sitio_original=original_snapshot,  
        campos_modificados=list(original_snapshot.keys()),
    )

    db.session.commit()
    return True

def export_sites_csv(filtros: dict = None):
    """
    Exporta la lista de sitios históricos en formato CSV.
    Aplica los mismos filtros que list_sites.
    """
    query = list_sites(filtros=filtros if filtros else {}, page=1, per_page=10000)
    if not query.items:
        return None
    
    output = StringIO()
    writer = csv.writer(output)

    # Encabezados
    writer.writerow([
        "ID", "Nombre", "Descripción Breve", "Ciudad", "Provincia", 
        "Latitud", "Longitud", "Estado de Conservación", "Fecha de registro", "Tags"
    ])

    for sitio in query.items:
        punto_shape = to_shape(sitio.punto) if sitio.punto else None
        latitud = punto_shape.y if punto_shape else None
        longitud = punto_shape.x if punto_shape else None

        writer.writerow([
            sitio.id,
            sitio.nombre,
            sitio.descripcion_breve,
            sitio.ciudad,
            sitio.provincia,
            latitud,
            longitud,
            sitio.estado_conservacion,
            sitio.created_at.strftime("%d/%m/%Y %H:%M"),
            ";".join(tag.name for tag in sitio.tags)
        ])

    output.seek(0)
    return output.getvalue()


def get_current_timestamp_str():
    """
    Retorna la fecha y hora actual en formato YYYYMMDD_HHMM para usar en nombres de archivo.
    """
    return datetime.now().strftime("%Y%m%d_%H%M")