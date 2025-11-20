from flask import Blueprint, request, jsonify
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import jwt
from datetime import datetime, timedelta
import os
from src.core.services.users import login_google as login_google_service
from . import api_bp
from flask import current_app as app


@api_bp.post("/login/google")
def login_with_google():
    """
    Inicia sesión o registra un usuario utilizando un token de Google.
    """
    
    if not request.is_json:
        return jsonify({"error": "Content-Type debe ser application/json"}), 400
    
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos en el cuerpo de la petición"}), 400
    
    token = data.get("id_token")

    if not token:
        return jsonify({
            "error": "Falta id_token",
            "received_data": list(data.keys()) if data else None
        }), 400

    # Verificar que GOOGLE_CLIENT_ID esté configurado
    google_client_id = app.config.get("GOOGLE_CLIENT_ID")
    if not google_client_id:
        return jsonify({"error": "GOOGLE_CLIENT_ID no está configurado en el servidor"}), 500
    
    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            google_client_id
        )
    except ValueError as e:
        app.logger.error(f"Error de valor al verificar token de Google: {e}")
        return jsonify({"error": "Token inválido o expirado", "details": str(e)}), 401
    except Exception as e:
        app.logger.error(f"Excepción inesperada al verificar token de Google: {e}", exc_info=True)
        return jsonify({"error": "Error al verificar el token de Google", "details": str(e)}), 401

    # Crear o recuperar usuario
    try:
        user = login_google_service(idinfo)
        if not user or not user.get("id"):
            return jsonify({"error": "Error al crear o recuperar el usuario"}), 500
    except Exception as e:
        return jsonify({"error": "Error al procesar el usuario", "details": str(e)}), 500

    # Verificar configuración de JWT
    jwt_secret = app.config.get("JWT_SECRET")
    jwt_algorithm = app.config.get("JWT_ALGORITHM", "HS256")
    
    if not jwt_secret:
        return jsonify({"error": "JWT_SECRET no está configurado en el servidor"}), 500

    # Crear token JWT
    try:
        payload = {
            "sub": str(user["id"]),
            "email": idinfo["email"],
            "name": idinfo.get("name"),
            
            "exp": datetime.utcnow() + timedelta(hours=1),
        }
        user["picture"] = idinfo.get("picture")
        jwt_token = jwt.encode(payload, jwt_secret, algorithm=jwt_algorithm)
        
       
        if isinstance(jwt_token, bytes):
            jwt_token = jwt_token.decode("utf-8")
    except Exception as e:
        return jsonify({"error": "Error al generar el token JWT", "details": str(e)}), 500

    return jsonify({
        "token": jwt_token,
        "user": user
    }), 200
