"""
Este controlador maneja las rutas relacionadas con las operaciones de sitios históricos.
"""
from src.core.services.upload_service import upload_file
from flask import Blueprint
from flask import render_template, request, redirect, url_for

from src.core.services import sites as board_sites
from src.core.services import tags as board_tags
from flask import session
from src.core.services.sites import list_sites, add_site, get_site, modify_site
from src.core.services.tags import list_tags
from flask import flash
from src.core.siteForm import SiteForm
import pycountry
from flask import current_app as app
from src.core.auth import login_required,permission_required
bp = Blueprint("sites", __name__, url_prefix="/sitios")

provincias_arg = [sub.name for sub in pycountry.subdivisions.get(country_code="AR")]


def process_uploaded_images():
    """Procesa las imágenes subidas desde el formulario y retorna un diccionario con los datos."""
    params = {}
    if "images" in request.files:
        images = request.files.getlist("images")
        images_alts = request.form.getlist("images_alts[]")
        images_descriptions = request.form.getlist("images_descriptions[]")
        uploaded_images = []
        for i, image in enumerate(images):
            if image.filename == "":
                continue
            object_name = upload_file(image, folder_name="sites")
            if not object_name:
                continue  # Si falla la subida, saltar esta imagen
            image_data = {
                "url": object_name,
                "title": images_alts[i] if i < len(images_alts) else "",
                "description": images_descriptions[i] if i < len(images_descriptions) else "",
                "order": i,
                "is_cover": False
            }
            # Validar que el título no esté vacío
            if not image_data["title"] or not image_data["title"].strip():
                raise ValueError("Todas las imágenes deben tener un título")
            uploaded_images.append(image_data)
        params["images"] = uploaded_images
        
        # Obtener índice de portada si viene en el formulario
        cover_index = request.form.get("cover_index")
        if cover_index and cover_index.isdigit():
            params["cover_index"] = int(cover_index)
    return params


@bp.get("/")
@permission_required('site_index')
@login_required
def index():
    """
    Muestra la lista de sitios históricos.
    """
    page = request.args.get("page", 1, type=int)
    per_page = 25

    filtros = request.args.to_dict()
    filtros.pop("page", None)
    filtros.pop("per_page", None)

    # Ya devuelve un objeto paginado
    try:
        pagination = board_sites.list_sites(filtros, page=page, per_page=per_page,include_cover=True)
        
    except ValueError as e:
        flash(str(e),"error")
        pagination= board_sites.list_sites({},page=page,per_page=per_page)
    tags = [{"value": tag.id, "label": tag.name} for tag in board_tags.list_tags()]
    #el filtro de provincias necesita las provincias en formato {'value': 'Buenos Aires', 'label': 'Buenos Aires'}
    provincias_arg = [
    {"value": sub.name, "label": sub.name}
    for sub in pycountry.subdivisions.get(country_code="AR")
]

    return render_template(
        "sites/sites_table.html",
        items=pagination.items,
        provincias=provincias_arg,
        pagination=pagination,
        filtros=filtros,
        tags=tags,
        order=request.args.get("order", None)
    )



@bp.route("/nuevo", methods=["GET", "POST"])
@permission_required("site_new")
@login_required
def add_site():
    """
    GET: muestra el formulario para crear un nuevo sitio histórico.
    POST: procesa el formulario y crea el sitio.
    
    
    """
    siteForm = SiteForm()

    # Provincias
    provincias_opts = [(prov, prov) for prov in provincias_arg]
    siteForm.provincia.choices = provincias_opts

    # Tags
    tags = [(tag.id, tag.name) for tag in board_tags.list_tags()]
    siteForm.tags.choices = tags

    if siteForm.tags.data is None:
        siteForm.tags.data = []

    try:
        # Procesar POST
        if siteForm.validate_on_submit():
            
            tags_seleccionados = request.form.getlist("tags[]")

            # images_alts = request.form.getlist("image_alt[]")
            params = process_uploaded_images()

            site_data = {
                "nombre": siteForm.nombre.data,
                "descripcion_breve": siteForm.descripcion_breve.data,
                "descripcion_completa": siteForm.descripcion_completa.data,
                "ciudad": siteForm.ciudad.data,
                "provincia": siteForm.provincia.data,
                "inauguracion": siteForm.inauguracion.data,
                "visible": siteForm.visible.data,
                "categoria": siteForm.categoria.data,
                "estado_conservacion": siteForm.estado_conservacion.data,
                "latitud": float(siteForm.latitud.data) if siteForm.latitud.data else None,
                "longitud": float(siteForm.longitud.data) if siteForm.longitud.data else None,
                "tags": [int(t) for t in tags_seleccionados], 
                "images": params.get("images", []),
            }

            user_id = session.get("user_id")
            board_sites.add_site(site_data, user_id)

            flash("Sitio histórico creado exitosamente.", "success")
            return redirect(url_for("sites.index"))

    except Exception as e:
        flash(str(e), "error")

    # Renderizar formulario
    return render_template(
        "sites/add_site.html",
        form=siteForm,
        provincias=provincias_opts,
        tags=tags
    )


@bp.route("/modificar/<int:site_id>", methods=["GET", "POST"])
@permission_required('site_update')
@login_required
def modify(site_id):
    """
    GET: muestra el formulario para modificar un sitio histórico.
    POST: procesa el formulario y actualiza el sitio.
    """
    
    try:
        site = board_sites.get_site(site_id, include_images=True)
        form = SiteForm(obj=site)
        form.provincia.choices = [(p, p) for p in provincias_arg]
        form.tags.choices = [(t.id, t.name) for t in board_tags.list_tags()]
        form.tags.data = [t.id for t in site.tags] 

        if form.validate_on_submit():
            user_id=session.get("user_id")
            data = form.data
            data["tags"] = request.form.getlist("tags[]")
            
            # Procesar imágenes nuevas si se suben
            params = process_uploaded_images()
            data["images"] = params.get("images", [])
            # Si no hay imágenes existentes, usar cover_index de las nuevas imágenes
            # Si hay imágenes existentes pero el usuario marcó una nueva como portada, también usar cover_index
            if not site.images_data:
                data["cover_index"] = params.get("cover_index")
            elif "cover_index" in params:
                # Hay imágenes existentes pero el usuario marcó una nueva como portada (reemplazará a la existente)
                data["cover_index"] = params.get("cover_index")
            
            # pasar el orden de imágenes existentes (si viene) al servicio
            order_payload = request.form.get('existing_images_order')
            if order_payload:
                data["existing_images_order"] = order_payload
            
            # Capturar metadatos de imágenes existentes (títulos y descripciones)
            existing_titles = {}
            existing_descriptions = {}
            for key, value in request.form.items():
                if key.startswith('existing_image_titles['):
                    # Extraer el ID de la imagen del formato existing_image_titles[123]
                    img_id = key.split('[')[1].rstrip(']')
                    existing_titles[img_id] = value
                elif key.startswith('existing_image_descriptions['):
                    img_id = key.split('[')[1].rstrip(']')
                    existing_descriptions[img_id] = value
            
            if existing_titles:
                data["existing_image_titles"] = existing_titles
            if existing_descriptions:
                data["existing_image_descriptions"] = existing_descriptions
            
            board_sites.modify_site(site_id, data, user_id)
            flash("Sitio actualizado correctamente.", "success")
            return redirect(url_for("sites.index"))
    except Exception as e:
        flash(str(e),"error")

    return render_template("sites/modify_site.html", form=form, site=site)


@bp.post("/eliminar/<int:site_id>")
@login_required
@permission_required('site_destroy')
def delete(site_id):
    """
    Elimina un sitio histórico.
    """
    try:
        sitio = board_sites.get_site(site_id)

        if not sitio:
            return render_template("404.html"), 404
        user_id=session.get("user_id")
        board_sites.delete_site(site_id,user_id)
        flash("Sitio histórico eliminado exitosamente.", "success")
    except Exception as e:
        flash(str(e),"error")
    return redirect(url_for("sites.index"))


@bp.post("/<int:site_id>/images/<int:image_id>/delete")
@login_required
@permission_required('site_update')
def delete_image(site_id, image_id):
    """Elimina una imagen del sitio (usado en la edición)."""
    try:
        board_sites.delete_site_image(site_id, image_id)
        flash("Imagen eliminada exitosamente.", "success")
    except Exception as e:
        flash(str(e), "error")
    return redirect(url_for("sites.modify", site_id=site_id))

@bp.post("/<int:site_id>/images/<int:image_id>/set-cover")
@login_required
@permission_required('site_update')
def set_cover_image(site_id, image_id):
    """Marca una imagen como portada del sitio."""
    try:
        board_sites.set_cover_image(site_id, image_id)
        flash("Imagen establecida como portada exitosamente.", "success")
    except Exception as e:
        flash(str(e), "error")
    return redirect(url_for("sites.modify", site_id=site_id))

@bp.get("/exportar")
@login_required
@permission_required('site_export')
def export():
    """
    Exporta la lista de sitios históricos en formato CSV.
    """
    filtros = request.args.to_dict()
    filtros.pop("exportar", None)

    csv_data = board_sites.export_sites_csv(filtros if len(filtros.keys()) > 0 else None)
    if csv_data is None:
        flash("No hay datos para exportar", "error")
        return redirect(url_for("sites.index",  **(filtros or {})))
    else:
        # Nos aseguramos de que csv_data sea una cadena (str) antes de codificar
        if not isinstance(csv_data, str):
            # Si export_sites_csv devuelve otra cosa, conviértela a string
            csv_data = str(csv_data) 

        response = app.response_class(
            # 1. Codificar la respuesta a bytes usando 'utf-8-sig' para compatibilidad con Excel
            response=csv_data.encode('utf-8-sig'),
            status=200,
            # 2. Especificar el charset en el mimetype
            mimetype="text/csv; charset=utf-8",
        )
        response.headers.set(
            "Content-Disposition",
            "attachment",
            filename=f"sitios_{board_sites.get_current_timestamp_str()}.csv",
        )

        return response
        


@bp.route("/<int:sitio_id>")
@permission_required('site_show')
@login_required
def detail(sitio_id):
    """
    renderiza los detalles del sitio
    """
  
    sitio = board_sites.get_site(sitio_id,include_cover=True)
    return render_template("sites/detail.html", sitio=sitio)
  

