from flask import jsonify,request
from . import api_bp

@api_bp.post("login/google")
def login_with_google():
    pass

@api_bp.get("login/google/callback")
def google_login_callback():
    pass

@api_bp.post("logout")
def logout():
    pass

@api_bp.get("user/profile")
def get_user_profile():
    pass