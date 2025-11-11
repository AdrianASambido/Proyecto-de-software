from functools import wraps
from flask import request, jsonify, current_app
import jwt


def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", None)

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token de autenticación requerido"}), 401

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(
                token,
                current_app.config["JWT_SECRET"],
                algorithms=["HS256"]
            )
            request.jwt_user = payload

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401
        except Exception:
            return jsonify({"error": "Error al validar token"}), 401

        return f(*args, **kwargs)
    return decorated


def get_current_user_from_jwt():
    if hasattr(request, 'jwt_user'):
        user_id = request.jwt_user.get('sub')
        if user_id:
            return int(user_id)
    return None
