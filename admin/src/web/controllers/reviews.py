from flask import render_template, Blueprint, request, redirect, url_for, flash, jsonify
from src.core.services.reviews import (
    list_reviews as svc_list_reviews,
    get_review as svc_get_review,
    approve_review as svc_approve_review,
    reject_review as svc_reject_review,
    delete_review as svc_delete_review,
    get_all_sites as svc_get_all_sites,
)
from src.core.auth import login_required, permission_required


bp = Blueprint("reviews", __name__, url_prefix="/resenias")


@bp.get("/")
@permission_required("review_index")
@login_required
def index():
    """Muestra el listado paginado de reseñas con filtros opcionales."""
    page = request.args.get("page", 1, type=int)
    per_page = 25

    filtros = request.args.to_dict()
    filtros.pop("page", None)
    filtros.pop("per_page", None)

    pagination = svc_list_reviews(filtros, page=page, per_page=per_page)

    # Obtener todos los sitios para el filtro
    sites = svc_get_all_sites()

    return (
        render_template(
            "reviews/reviews_table.html",
            items=pagination.items,
            pagination=pagination,
            filtros=filtros,
            sites=sites,
        ),
        200,
    )


@bp.get("/<int:review_id>")
@permission_required("review_show")
@login_required
def show(review_id):
    """Muestra el detalle de una reseña."""
    review = svc_get_review(review_id)
    if not review:
        flash("Reseña no encontrada.", "error")
        return redirect(url_for("reviews.index"))

    return render_template("reviews/detail.html", review=review)


@bp.post("/<int:review_id>/aprobar")
@permission_required("review_approve")
@login_required
def approve(review_id):
    """Aprueba una reseña."""
    try:
        review = svc_approve_review(review_id)
        flash(f"Reseña #{review.id} aprobada exitosamente.", "success")
    except ValueError as e:
        flash(str(e), "error")

    return redirect(url_for("reviews.index"))


@bp.post("/<int:review_id>/rechazar")
@permission_required("review_reject")
@login_required
def reject(review_id):
    """Rechaza una reseña con un motivo."""
    motivo = request.form.get("motivo_rechazo", "").strip()

    try:
        review = svc_reject_review(review_id, motivo)
        flash(f"Reseña #{review.id} rechazada exitosamente.", "success")
    except ValueError as e:
        flash(str(e), "error")

    return redirect(url_for("reviews.index"))


@bp.post("/<int:review_id>/eliminar")
@permission_required("review_destroy")
@login_required
def delete(review_id):
    """Elimina una reseña de forma permanente."""
    try:
        # Obtener información de la reseña antes de eliminarla
        review = svc_get_review(review_id)
        if review:
            svc_delete_review(review_id)
            flash(f"Reseña #{review.id} eliminada permanentemente.", "success")
        else:
            flash("Reseña no encontrada.", "error")
    except ValueError as e:
        flash(str(e), "error")

    return redirect(url_for("reviews.index"))
