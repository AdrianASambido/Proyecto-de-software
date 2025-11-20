from flask import jsonify, request
# from flask_jwt_extended import jwt_required, get_jwt_identity
from . import api_bp
from .auth import jwt_required, get_current_user_from_jwt
from src.core.services.reviews import (
    list_reviews,
    create_review,
    get_review_by_site,
    delete_review,
    update_review
)

@api_bp.get("sites/<int:site_id>/reviews")
def get_reviews_for_site(site_id):
    """
    Lista las reseñas APROBADAS de un sitio con paginación.
    """
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 25))

        filtros = {
            "estado": "APROBADA",
            "site_id": site_id
        }

        reviews_pag = list_reviews(filtros, page=page, per_page=per_page)

        data = [review.to_dict() for review in reviews_pag.items]

        response = {
            "data": data,
            "meta": {
                "page": reviews_pag.page,
                "per_page": reviews_pag.per_page,
                "total": reviews_pag.total
            }
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.post("sites/<int:site_id>/reviews")
@jwt_required
def add_review_to_site(site_id):
    try:
       
       """
        Agrega una nueva reseña a un sitio.
        """
        data = request.get_json()

        if not data:
            return jsonify({"error": "No se proporcionó información en el body"}), 400

        user_id = get_current_user_from_jwt()
        if not user_id:
            return jsonify({"error": "Usuario no autenticado"}), 401

        calificacion = data.get("calificacion")
        contenido = data.get("contenido")

        if calificacion is None:
            return jsonify({"error": "El campo 'calificacion' es requerido"}), 400
        if not contenido:
            return jsonify({"error": "El campo 'contenido' es requerido"}), 400

        # Convertir calificacion a entero y validar
        try:
            calificacion = int(calificacion)
            if calificacion < 1 or calificacion > 5:
                return jsonify({"error": "La calificación debe ser un número entre 1 y 5"}), 400
        except (ValueError, TypeError):
            return jsonify({"error": "La calificación debe ser un número válido"}), 400

        review = create_review(site_id, user_id, calificacion, contenido)

        return jsonify(review.to_dict()), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.get("sites/<int:site_id>/reviews/<int:review_id>")
def get_review_by_id(site_id, review_id):
    """
    Obtiene una reseña específica de un sitio.
    """
    try:
        review = get_review_by_site(site_id, review_id)

        if not review:
            return jsonify({"error": "Reseña no encontrada"}), 404

        return jsonify(review.to_dict()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.delete("sites/<int:site_id>/reviews/<int:review_id>")
@jwt_required
def delete_review_endpoint(site_id, review_id):
    """
    Elimina una reseña específica de un sitio.
    """
    try:
        user_id = get_current_user_from_jwt()
        review = get_review_by_site(site_id, review_id)

        if not review:
            return jsonify({"error": "Reseña no encontrada"}), 404

        if review.user_id != user_id:
            return jsonify({"error": "No tiene permisos para eliminar esta reseña"}), 403

        delete_review(review_id)

        return jsonify({"message": "Reseña eliminada exitosamente"}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.put("sites/<int:site_id>/reviews/<int:review_id>")
@jwt_required
def update_review_endpoint(site_id, review_id):
    """
    Actualiza una reseña específica de un sitio.
    """
    try:
        user_id = get_current_user_from_jwt()
        data = request.get_json()

        if not data:
            return jsonify({"error": "No se proporcionó información en el body"}), 400

        calificacion = data.get("calificacion")
        contenido = data.get("contenido")

        if calificacion is None:
            return jsonify({"error": "El campo 'calificacion' es requerido"}), 400
        if not contenido:
            return jsonify({"error": "El campo 'contenido' es requerido"}), 400

        review = update_review(site_id, review_id, user_id, calificacion, contenido)

        return jsonify(review.to_dict()), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.get("me/reviews")
@jwt_required
def get_my_reviews():
    """
    Lista las reseñas del usuario autenticado con paginación.
    """
    try:
        user_id = get_current_user_from_jwt()
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 25))

        order = request.args.get("order", "fecha_desc")

        filtros = {
            "user_id": user_id,
            "order": order
        }
        reviews_pag = list_reviews(filtros, page=page, per_page=per_page)

        data = []
        for review in reviews_pag.items:
            review_dict = review.to_dict()
            review_dict["site"] = {
                "id": review.site.id,
                "nombre": review.site.nombre,
                "ciudad": review.site.ciudad,
                "provincia": review.site.provincia
            }
            data.append(review_dict)

        response = {
            "data": data,
            "meta": {
                "page": reviews_pag.page,
                "per_page": reviews_pag.per_page,
                "total": reviews_pag.total
            }
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500