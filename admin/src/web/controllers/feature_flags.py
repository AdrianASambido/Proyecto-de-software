"""
Controlador para Feature Flags
Maneja las rutas relacionadas con la gestión de feature flags
"""

from flask import Blueprint, render_template, request, jsonify
from src.core.services.feature_flags import list_feature_flags, update_feature_flag, get_feature_flag_by_name

bp = Blueprint("feature_flags", __name__, url_prefix="/admin/feature-flags")

@bp.get("/")
def index():
    """
    Muestra la lista de feature flags
    """
    flags = list_feature_flags()
    return render_template("administration/feature_flags.html", flags=flags), 200

@bp.post("/toggle/<int:flag_id>")
def toggle_flag(flag_id):
    """
    Cambia el estado de un feature flag
    """
    data = request.get_json()
    is_enabled = data.get('is_enabled', False)
    maintenance_message = data.get('maintenance_message', '')
    modified_by = data.get('modified_by', 'System Admin')  # Por ahora hardcodeado
    
    success = update_feature_flag(
        flag_id=flag_id,
        is_enabled=is_enabled,
        maintenance_message=maintenance_message,
        modified_by=modified_by
    )
    
    if success:
        return jsonify({'success': True, 'message': 'Feature flag actualizado correctamente'})
    else:
        return jsonify({'success': False, 'message': 'Error al actualizar el feature flag'}), 400

@bp.get("/status")
def get_flags_status():
    """
    Obtiene el estado actual de todos los flags (API endpoint)
    """
    flags = list_feature_flags()
    status = {}
    
    for flag in flags:
        status[flag.name] = {
            'is_enabled': flag.is_enabled,
            'maintenance_message': flag.maintenance_message
        }
    
    return jsonify(status)
