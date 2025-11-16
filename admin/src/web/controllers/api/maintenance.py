from flask import jsonify
from . import api_bp
from src.core.services.feature_flags import (
    is_portal_maintenance_mode,
    get_portal_maintenance_message
)
@api_bp.get("/system/maintenance")
def is_in_maintenance():
    maintenance = is_portal_maintenance_mode()

    return jsonify({
        "maintenance": maintenance,
        "message": get_portal_maintenance_message() if maintenance else ""
    }), 200
