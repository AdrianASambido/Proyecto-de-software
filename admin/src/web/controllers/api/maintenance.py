from flask import jsonify
from . import api_bp
from src.core.services.feature_flags import (
    is_portal_maintenance_mode,
    get_portal_maintenance_message
    ,are_reviews_enabled as are_reviews_enabled_service
)
@api_bp.get("/system/maintenance")
def is_in_maintenance():

    """
    Verifica si el portal está en modo de mantenimiento.
    """
    maintenance = is_portal_maintenance_mode()

    return jsonify({
        "maintenance": maintenance,
        "message": get_portal_maintenance_message() if maintenance else ""
    }), 200


@api_bp.get("/system/reviews_enabled")
def are_reviews_enabled():
    """
    Verifica si la funcionalidad de reseñas está habilitada.
    """
    
    enabled = are_reviews_enabled_service()

    return jsonify({
        "reviews_enabled": enabled
    }), 200