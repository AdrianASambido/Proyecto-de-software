"""
    Este modelo representa las operaciones relacionadas con los feature flags.
"""

from src.core.database import db
from src.core.Entities.feature_flag import FeatureFlag
from datetime import datetime, timezone


def list_feature_flags():
    """
    Retorna una lista de todos los feature flags.
    """
    flags = FeatureFlag.query.all()
    return flags


def get_feature_flag_by_name(name):
    """
    Obtiene un feature flag por su nombre
    """
    return FeatureFlag.query.filter_by(name=name).first()


def update_feature_flag(
    flag_id, is_enabled, maintenance_message=None, modified_by=None
):
    """
    Actualiza el estado de un feature flag
    """
    flag = FeatureFlag.query.get(flag_id)
    if not flag:
        return False

    flag.is_enabled = is_enabled
    if maintenance_message is not None:
        flag.maintenance_message = maintenance_message
    if modified_by:
        flag.last_modified_by = modified_by
    flag.last_modified_at = datetime.now(timezone.utc)

    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error updating feature flag: {e}")
        return False


def is_admin_maintenance_mode():
    """
    Verifica si el modo mantenimiento de administración está activo
    """
    flag = get_feature_flag_by_name("admin_maintenance_mode")
    return flag.is_enabled if flag else False


def is_portal_maintenance_mode():
    """
    Verifica si el modo mantenimiento del portal está activo
    """
    flag = get_feature_flag_by_name("portal_maintenance_mode")
    return flag.is_enabled if flag else False


def are_reviews_enabled():
    """
    Verifica si las reseñas están habilitadas
    """
    flag = get_feature_flag_by_name("reviews_enabled")
    return flag.is_enabled if flag else True  # Por defecto habilitadas


def get_admin_maintenance_message():
    """
    Obtiene el mensaje de mantenimiento para administración
    """
    flag = get_feature_flag_by_name("admin_maintenance_mode")
    return flag.maintenance_message if flag else "Sistema en mantenimiento"


def get_portal_maintenance_message():
    """
    Obtiene el mensaje de mantenimiento para el portal
    """
    flag = get_feature_flag_by_name("portal_maintenance_mode")
    return flag.maintenance_message if flag else "Portal en mantenimiento"
