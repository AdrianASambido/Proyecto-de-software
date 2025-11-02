from flask import jsonify,request
from . import api_bp

@api_bp.post("login/google")
def login_with_google():
    """Autenticar con google"""

    pass

@api_bp.get("login/google/callback")
def google_login_callback():
    """Callback de google"""
    pass

@api_bp.post("logout")
def logout():
    """Cerrar sesión del usuario"""
    pass