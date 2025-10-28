
from flask import jsonify,request
from . import api_bp
from flask_jwt_extended import jwt_required, get_jwt_identity
from core.services.users import add_favorite_site,remove_favorite_site,get_favorite_sites
from core.services.users import get_user_by_email
from core.services.sites import get_site


@api_bp.put("sites/<int:site_id>/favorite")
@jwt_required()
def favorite():
    user_email=get_jwt_identity()
    user=get_user_by_email(user_email)
    if not user:
        return jsonify({"msg":"Usuario no encontrado"}),404
    
    site=get_site(site_id)
    if not site:
        return jsonify({"msg":"Sitio no encontrado"}),404

    if site in user.favorites:

        return "", 204

    add_favorite_site(user,site)
    return jsonify({"msg":"Sitio agregado a favoritos"}),204
    


@api_bp.delete("sites/<int:site_id>/favorite")
@jwt_required()
def unfavorite():
    user_email=get_jwt_identity()
    user=get_user_by_email(user_email)
    if not user:
        return jsonify({"msg":"Usuario no encontrado"}),404
    
    site=get_site(site_id)
    if not site:
        return jsonify({"msg":"Sitio no encontrado"}),404

    if site not in user.favorites:

        return "", 204

    remove_favorite_site(user,site)
   
    return jsonify({"msg":"Sitio removido de favoritos"}),204
