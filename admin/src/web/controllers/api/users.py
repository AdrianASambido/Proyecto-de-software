from flask import jsonify, request
from . import api_bp
# from flask_jwt_extended import jwt_required
from src.core.services.users import add_favorite_site, remove_favorite_site, get_user_by_email
from src.core.services.users import is_favorite as is_favorite_service
from src.core.services.sites import get_site

@api_bp.put("/sites/<int:site_id>/favorite")
# @jwt_required()
def favorite(site_id):
    user_email = request.args.get("email", "test@example.com")
    user = get_user_by_email(user_email)
    if not user:
        return jsonify({"msg": f"Usuario '{user_email}' no encontrado"}), 404

    site = get_site(site_id)
    if not site:
        return jsonify({"msg": "Sitio no encontrado"}), 404

    if add_favorite_site(user.id, site.id):
        return jsonify({"msg": "Sitio agregado a favoritos"}), 201
    else:
        return jsonify({"msg": "El sitio ya estaba en favoritos"}), 200


@api_bp.delete("/sites/<int:site_id>/favorite")
# @jwt_required()
def unfavorite(site_id):
    user_email = request.args.get("email", "test@example.com")
    user = get_user_by_email(user_email)
    if not user:
        return jsonify({"msg": f"Usuario '{user_email}' no encontrado"}), 404

    site = get_site(site_id)
    if not site:
        return jsonify({"msg": "Sitio no encontrado"}), 404

    if remove_favorite_site(user.id, site.id):
        return jsonify({"msg": "Sitio removido de favoritos"}), 200
    else:
        return jsonify({"msg": "El sitio no estaba en favoritos"}), 200


@api_bp.get("/sites/<int:site_id>/favorite")
def is_favorite(site_id):
    user_email = request.args.get("email")
    user = get_user_by_email(user_email)
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    site = get_site(site_id)
    if not site:
        return jsonify({"msg": "Sitio no encontrado"}), 404

    
    is_fav = is_favorite_service(user.id, site.id)

    return jsonify({"favorite": is_fav}), 200
