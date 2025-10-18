from flask import jsonify,request
from . import api_bp
from src.core.services.sites import list_sites,add_site,get_site

@api_bp.get("/sites")
def get_sites():
   
    filtros = request.args.to_dict(flat=True)

    page = int(filtros.pop("page", 1))
    per_page = int(filtros.pop("per_page", 25))
    
    if "tags" in filtros:
        filtros["tags"] = filtros["tags"].split(",")
    
    sitios_pag = list_sites(filtros, page=page, per_page=per_page)

    data = [s.to_dict() for s in sitios_pag.items]

    response = {
        "data": data,
        "meta": {
            "page": sitios_pag.page,
            "per_page": sitios_pag.per_page,
            "total": sitios_pag.total
        }
    }
    
    return jsonify(response)


@api_bp.get("/sites/<int:site_id>")
def get_site_by_id(site_id):
    site = get_site(site_id)
    if not site:
        return jsonify({"error": "Sitio no encontrado"}), 404
    return jsonify(site.to_dict()), 200