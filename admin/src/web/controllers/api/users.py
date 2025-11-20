from flask import jsonify, request
from . import api_bp
from .auth import jwt_required, get_current_user_from_jwt
from src.core.services.users import add_favorite_site, remove_favorite_site, get_user_by_id
from src.core.services.users import is_favorite as is_favorite_service
from src.core.services.sites import get_site, list_sites
from src.web.controllers.api.schemas.site import SiteSchema
    
    
@api_bp.put("/sites/<int:site_id>/favorite")
@jwt_required
def favorite(site_id):
    """
    Marca un sitio como favorito para el usuario autenticado.
    """
    user_id = get_current_user_from_jwt()
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"msg": f"Usuario '{user_id}' no encontrado"}), 404

    site = get_site(site_id)
    if not site:
        return jsonify({"msg": "Sitio no encontrado"}), 404

    if add_favorite_site(user.id, site.id):
        return jsonify({"msg": "Sitio agregado a favoritos"}), 201
    else:
        return jsonify({"msg": "El sitio ya estaba en favoritos"}), 200


@api_bp.delete("/sites/<int:site_id>/favorite")
@jwt_required
def unfavorite(site_id):
    """
    Remueve un sitio de los favoritos del usuario autenticado.
    """
    user_id = get_current_user_from_jwt()
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"msg": f"Usuario '{user_id}' no encontrado"}), 404

    site = get_site(site_id)
    if not site:
        return jsonify({"msg": "Sitio no encontrado"}), 404

    if remove_favorite_site(user_id, site.id):
        return jsonify({"msg": "Sitio removido de favoritos"}), 200
    else:
        return jsonify({"msg": "El sitio no estaba en favoritos"}), 200


@api_bp.get("/sites/<int:site_id>/favorite")
def is_favorite(site_id):
    """
    Verifica si un sitio es favorito para un usuario específico.
    """
    user_id = request.args.get("userId", type=int)
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    site = get_site(site_id)
    if not site:
        return jsonify({"msg": "Sitio no encontrado"}), 404

    
    is_fav = is_favorite_service(user.id, site.id)

    return jsonify({"favorite": is_fav}), 200

@api_bp.get("/me/favorites")
@jwt_required
def get_favorites():
    """
    Lista los sitios favoritos del usuario autenticado con paginación.
    """
    user_id = get_current_user_from_jwt()
    if not user_id:
        return jsonify({"error": "Token sin sub"}), 401

    filtros = {k.lower(): v for k, v in request.args.to_dict(flat=True).items()}
    page = int(filtros.pop("page", 1))
    per_page = int(filtros.pop("per_page", 25))
    include_cover = filtros.pop("include_cover", "true").lower() in ("true", "1", "yes")
    order = filtros.pop("order", "fecha_desc")  # por defecto más recientes
    filtros["order"] = order
    filtros["visible"] = True
    # Solo filtrar los sitios que el usuario marcó como favorito
    filtros["favoritos"] = True
    filtros["user_id"] = user_id

    # Cargar los sitios con orden por created_at
    sitios_pag = list_sites(filtros, page=page, per_page=per_page, include_cover=include_cover)

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

    return jsonify(response), 200

