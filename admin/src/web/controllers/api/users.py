from flask import jsonify, request
from . import api_bp
import os
from functools import wraps
import jwt 
from flask_jwt_extended import jwt_required
from src.core.services.users import add_favorite_site, remove_favorite_site, get_user_by_email
from src.core.services.users import is_favorite as is_favorite_service
from src.core.services.sites import get_site, list_sites
from flask import current_app as app

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print("SECRET:", app.config["JWT_SECRET"])

        auth_header = request.headers.get("Authorization", None)
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Falta token o formato inválido"}), 401

        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, app.config["JWT_SECRET"], algorithms=[app.config["JWT_ALGORITHM"]])
            request.user = payload  # Guardamos el payload en la request
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401

        return f(*args, **kwargs)
    return decorated
    
@api_bp.put("/sites/<int:site_id>/favorite")
@require_auth
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
@require_auth
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

@api_bp.get("/me/favorites")
@require_auth
def get_favorites():
   
    user_id = request.user.get("sub")
    if not user_id:
        return jsonify({"error": "Token sin sub"}), 401

    filtros = {k.lower(): v for k, v in request.args.to_dict(flat=True).items()}
    page = int(filtros.pop("page", 1))
    per_page = int(filtros.pop("per_page", 25))
    include_cover = filtros.pop("include_cover", "false").lower() in ("true", "1", "yes")

    filtros["favoritos"] = True
    filtros["user_id"] = user_id 

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

