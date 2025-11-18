"""
Este modelo representa las operaciones relacionadas con los sitios historicos.
"""

from src.core.database import db
from src.core.Entities.site import Site
from src.core.Entities.review import Review,ReviewStatus
from src.core.Entities.site_history import HistoryAction
from src.core.Entities.user import User

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
from flask import current_app
import json
from src.core.services.upload_service import delete_file as delete_minio_file

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
            db.session.query(
                Cover.site_id,
                func.max(Cover.url).label("url")
            )
            .filter(Cover.is_cover == True)
            .group_by(Cover.site_id)
            .subquery()
        )

        query = query.outerjoin(subquery, Site.id == subquery.c.site_id)
        pagination = query.add_columns(subquery.c.url.label("cover_url")).paginate(
            page=page, per_page=per_page, error_out=False
        )

        results = []
        for site, cover_url in pagination.items:
            site._cover_url = f"http://{current_app.config['MINIO_SERVER']}/{current_app.config['MINIO_BUCKET']}/{cover_url}" if cover_url else None  
            # sort_site_images(site)
            results.append(site)

        pagination.items = results
        return pagination

    return query.paginate(page=page, per_page=per_page, error_out=False)


def calculate_review_count(site_id):
    """
    Calcula la cantidad de reseñas aprobadas para un sitio histórico.
    """
    count = (
        db.session.query(func.count(Review.id))
        .filter(
            Review.site_id == site_id,
            Review.estado == ReviewStatus.APROBADA
        )
        .scalar()
    )
    return count

def calculate_valoration(site_id):
    """
    Calcula la valoración promedio de un sitio histórico basado en las reseñas aprobadas.
    """
    avg_valoration = (
        db.session.query(func.avg(Review.calificacion))
        .filter(
            Review.site_id == site_id,
            Review.estado == ReviewStatus.APROBADA
        )
        .scalar()
    )
    return round(avg_valoration, 2) if avg_valoration is not None else None


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

from sqlalchemy import func, and_
from sqlalchemy.orm import aliased

def order_sites(query, filtros):
    orden = filtros.get("order", "fecha_desc")

    if orden == "mejor_puntuado":
        avg_reviews_subq = (
            db.session.query(
                Review.site_id.label("site_id"),
                func.avg(Review.calificacion).label("promedio")
            )
            .filter(Review.estado == ReviewStatus.APROBADA)
            .group_by(Review.site_id)
            .subquery()
        )

        query = query.outerjoin(avg_reviews_subq, Site.id == avg_reviews_subq.c.site_id)
        query = query.order_by(avg_reviews_subq.c.promedio.desc().nullslast())
        return query

   
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

    # Filtro por favoritos y user_id
    if filtros.get("favoritos") and filtros.get("user_id"):
        user_id = filtros["user_id"]
     
        query = (
            query
            .join(Site.favorite_users)
            .filter(User.id == user_id)
        )
    

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

from flask import current_app

def get_site(site_id, include_images=False, include_cover=False):
    sitio = Site.query.get(site_id)
    if not sitio:
        return None

    # Construir URL base de MinIO directamente desde config existente
    minio_server = current_app.config.get("MINIO_SERVER", "localhost:9000")
    minio_secure = current_app.config.get("MINIO_SECURE", False)
    minio_bucket= current_app.config.get("MINIO_BUCKET", "grupo01")
    scheme = "https" if minio_secure else "http"
    base_url = f"{scheme}://{minio_server}/{minio_bucket}/"

    # Obtener la portada si se solicita
    if include_cover:
        cover_image = Image.query.filter_by(site_id=site_id, is_cover=True).first()
        if cover_image:
            sitio._cover_url = (
                f"{base_url}{cover_image.url}" 
                if not cover_image.url.startswith("http") 
                else cover_image.url
            )
        else:
            sitio._cover_url = None

   
    if include_images:
        sitio.images_data = [
            {
                "id": img.id,
                "url": (
                    f"{base_url}{img.url}"
                    if not img.url.startswith("http") 
                    else img.url
                ),
                "title": img.title,
                "description": img.description,
                "order": img.order,
                "is_cover": img.is_cover,
            }
            for img in sitio.images
        ]
        sort_site_images(sitio)
 
    sitio.tags_data = [
        {"id": tag.id, "nombre": tag.name}
        for tag in sitio.tags
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

    # Agregar imágenes nuevas si vienen
    images_data = site_data.get("images", [])
    if images_data:
        # Obtener el máximo order de las imágenes existentes
        existing_images = sitio.images
        existing_count = len(existing_images) if existing_images else 0
        new_count = len(images_data)
        
        # Validar límite total de 10 imágenes
        if existing_count + new_count > 10:
            raise ValueError(
                f"Máximo 10 imágenes por sitio. Ya tienes {existing_count} imagen(es), "
                f"intentas agregar {new_count}. Puedes agregar máximo {10 - existing_count} imagen(es) más."
            )
        
        max_order = max([img.order for img in existing_images if img.order is not None], default=-1) if existing_images else -1
        
        # Verificar si ya hay una imagen de portada
        has_cover = any(img.is_cover for img in existing_images) if existing_images else False
        
        # Crear y agregar las nuevas imágenes
        new_image_ids = []
        for idx, img_info in enumerate(images_data):
            nueva_imagen = Image(**img_info)
            nueva_imagen.site_id = sitio.id
            nueva_imagen.order = max_order + 1 + idx
            # Si se especifica un índice de portada, establecer esta imagen como portada
            cover_index = site_data.get("cover_index")
            if cover_index is not None and idx == cover_index:
                nueva_imagen.is_cover = True
                # Desmarcar otras imágenes como portada si esta es la nueva portada
                if existing_images:
                    for img in existing_images:
                        img.is_cover = False
            # Si no hay portada actual y es la primera imagen nueva, marcarla como portada
            elif not has_cover and idx == 0:
                nueva_imagen.is_cover = True
            db.session.add(nueva_imagen)
            db.session.flush()  # Para obtener el ID
            new_image_ids.append(nueva_imagen.id)
    
    db.session.commit()

    # Actualizar metadatos de imágenes existentes si vienen
    existing_titles = site_data.get("existing_image_titles", {})
    existing_descriptions = site_data.get("existing_image_descriptions", {})
    
    if existing_titles or existing_descriptions:
        for img_id_str, title in existing_titles.items():
            try:
                img_id = int(img_id_str)
                img = Image.query.filter_by(id=img_id, site_id=sitio.id).first()
                if img:
                    if not title or not title.strip():
                        raise ValueError(f"La imagen '{img.title or 'sin título'}' debe tener un título")
                    img.title = title.strip()
                    # Actualizar descripción si viene
                    if img_id_str in existing_descriptions:
                        img.description = existing_descriptions[img_id_str].strip() if existing_descriptions[img_id_str] else None
            except ValueError as e:
                raise e
            except Exception as e:
                current_app.logger.debug(f"Error al actualizar metadatos de imagen {img_id_str}: {e}")

    # Actualizar orden de imágenes existentes si viene
    order_payload = site_data.get("existing_images_order")
    try:
        if order_payload:
            # order_payload puede venir como JSON string o como lista ya
            if isinstance(order_payload, str):
                ids = json.loads(order_payload)
            else:
                ids = order_payload

            # actualizar order de cada imagen (solo si pertenece a este sitio)
            for idx, img_id in enumerate(ids):
                try:
                    img = Image.query.get(int(img_id))
                    if img and img.site_id == sitio.id:
                        img.order = idx
                except Exception:
                    current_app.logger.debug("skip invalid image id in ordering: %s", img_id)

        db.session.commit()
    except Exception:
        db.session.rollback()
        current_app.logger.exception("Error al modificar sitio y/o actualizar orden de imágenes")
        raise

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
    
    # Validar límite de 10 imágenes
    if len(images_data) > 10:
        raise ValueError(f"Máximo 10 imágenes por sitio. Intentas agregar {len(images_data)}.")
    
    # Validar que todas las imágenes tengan título
    for img_info in images_data:
        if not img_info.get("title") or not img_info["title"].strip():
            raise ValueError("Todas las imágenes deben tener un título")
    
    # crear las imagenes en la db y asociarlas
    for idx, img_info in enumerate(images_data):
        nueva_imagen = Image(**img_info)
        nuevo_sitio.images.append(nueva_imagen)
    
    # establecer la primera imagen como portada si hay imágenes
    if nuevo_sitio.images:
        nuevo_sitio.images[0].is_cover = True

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

def delete_site_image(site_id: int, image_id: int):
    """Elimina una imagen de un sitio. Si era portada, reasigna portada a la siguiente por orden."""
    sitio = Site.query.get(site_id)
    if not sitio:
        raise ValueError("Sitio no encontrado")
    
    # Verificar directamente que la imagen existe y pertenece al sitio
    imagen = Image.query.filter_by(id=image_id, site_id=site_id).first()
    if not imagen:
        # Verificar si la imagen existe pero pertenece a otro sitio
        imagen_existe = Image.query.get(image_id)
        if imagen_existe:
            raise ValueError("La imagen no pertenece al sitio")
        else:
            raise ValueError("Imagen no encontrada")

    # Verificar que no sea la portada antes de eliminar
    if imagen.is_cover:
        raise ValueError("No se puede eliminar la imagen portada. Debe cambiar la portada primero.")
    
    # Guardar la URL del archivo antes de eliminar
    object_name = imagen.url
    
    # Eliminar la imagen de la base de datos
    db.session.delete(imagen)
    db.session.commit()
    
    # Eliminar el archivo físico de MinIO
    if object_name:
        try:
            delete_minio_file(object_name)
        except Exception as e:
            current_app.logger.error(f"Error al eliminar archivo de MinIO {object_name}: {e}")
            # No lanzamos excepción porque la imagen ya se eliminó de la BD

def set_cover_image(site_id: int, image_id: int):
    """Marca una imagen como portada del sitio, desmarcando las demás."""
    sitio = Site.query.get(site_id)
    if not sitio:
        raise ValueError("Sitio no encontrado")
    
    # Verificar que la imagen existe y pertenece al sitio
    imagen = Image.query.filter_by(id=image_id, site_id=site_id).first()
    if not imagen:
        imagen_existe = Image.query.get(image_id)
        if imagen_existe:
            raise ValueError("La imagen no pertenece al sitio")
        else:
            raise ValueError("Imagen no encontrada")
    
    # Desmarcar todas las imágenes como portada
    for img in sitio.images:
        img.is_cover = False
    
    # Marcar la imagen seleccionada como portada
    imagen.is_cover = True
    
    db.session.commit()

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


def sort_site_images(sitio):
    """Asegura que sitio.images esté ordenado por Image.order (None -> 0)."""
    try:
        sitio.images = sorted(sitio.images, key=lambda im: (im.order if getattr(im, "order", None) is not None else 0))
    except Exception:
        # no fallar si algo raro sucede con la relación
        pass

