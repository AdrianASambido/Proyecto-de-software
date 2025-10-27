from flask import jsonify,request
from src.web.controllers.api.schemas.site import SiteSchema
from . import api_bp
from src.core.services.sites import list_sites,add_site,get_site

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
    site = get_site(site_id)
    if not site:
        return jsonify({"error": "Sitio no encontrado"}), 404

    schema = SiteSchema()
    data = schema.dump(site)
    return jsonify(data), 200