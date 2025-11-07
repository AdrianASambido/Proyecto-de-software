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
    
    # Si hay filtro de favoritos, verificar autenticación
    '''favoritos = filtros.get("favoritos")
    if favoritos and favoritos.lower() in ("true", "1", "yes"):
        try:
            verify_jwt_in_request_optional()
            user_email = get_jwt_identity()
            if user_email:
                user = get_user_by_email(user_email)
                if user:
                    filtros["user_id"] = user.id
                else:
                    # Si no se encuentra el usuario, remover el filtro de favoritos
                    filtros.pop("favoritos", None)
            else:
                # Si no hay token válido, remover el filtro de favoritos
                filtros.pop("favoritos", None)
        except:
            # Si hay error en la verificación, remover el filtro
            filtros.pop("favoritos", None)
    '''
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

    return jsonify(data), 200
