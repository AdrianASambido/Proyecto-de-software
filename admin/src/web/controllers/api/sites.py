from flask import jsonify,request
from src.web.controllers.api.schemas.site import SiteSchema
from . import api_bp
from src.core.services.sites import list_sites,add_site,get_site
#from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request_optional
from src.core.services.users import get_user_by_email

@api_bp.get("/sites")
def get_sites():
    filtros = {k.lower(): v for k, v in request.args.to_dict(flat=True).items()}
   

    page = int(filtros.pop("page", 1))
    per_page = int(filtros.pop("per_page", 25))
    
    if "tags" in filtros:
        filtros["tags"] = filtros["tags"].split(",")

    include_cover = filtros.pop("include_cover", "false").lower() in ("true", "1", "yes")
    
    
    sitios_pag = list_sites(filtros, page=page, per_page=per_page,include_cover=include_cover)

    schema = SiteSchema(many=True)
    data = schema.dump(sitios_pag.items)

    response = {
        "data": data,
        "meta": {
            "page": sitios_pag.page,
            "per_page": sitios_pag.per_page,
            "total": sitios_pag.total
        }
    }
    
    return jsonify(response),200

@api_bp.get("/sites/<int:site_id>")
def get_site_by_id(site_id):
    include_images = request.args.get("include_images", "false").lower() == "true"
    site = get_site(site_id, include_images=include_images)

    if not site:
        return jsonify({"error": "Sitio no encontrado"}), 404

    schema = SiteSchema()
    data = schema.dump(site)
    if data.get("valoracion_promedio") is not None:
        data["valoracion_promedio"] = float(data["valoracion_promedio"])
    else:   
        data["valoracion_promedio"] = 0.0
    if hasattr(site, "images_data"):
        data["imagenes"] = site.images_data
    if hasattr(site, "tags_data"):
        data["tags"] = site.tags_data

    return jsonify(data), 200
