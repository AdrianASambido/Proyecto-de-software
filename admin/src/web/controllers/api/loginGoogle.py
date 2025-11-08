from flask import Blueprint, request, jsonify
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import jwt, datetime, os
from src.core.services.users import login_google as login_google_service
from . import api_bp
from flask import current_app as app


@api_bp.post("/login/google")
def login_with_google():
    data = request.get_json()
    token = data.get("id_token")

    if not token:
        return jsonify({"error": "Falta id_token"}), 400

    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            app.config["GOOGLE_CLIENT_ID"]  
        )
    except Exception as e:
        return jsonify({"error": "Token inválido", "details": str(e)}), 401

  
   
    user = login_google_service(idinfo)


    payload = {
        "sub": user["id"],
        "email": idinfo["email"],
        "name": idinfo.get("name"),
      
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
    }
    print("SECRET:", app.config["JWT_SECRET"])

    jwt_token = jwt.encode(payload, app.config["JWT_SECRET"], algorithm=app.config["JWT_ALGORITHM"])
   

   
    if isinstance(jwt_token, bytes):
        jwt_token = jwt_token.decode("utf-8")


    return jsonify({"token": jwt_token, "user": user}), 200
