from flask import render_template, Blueprint, request, redirect, url_for, flash
from src.core.services.tags import (
    list_tags as svc_list_tags,
    add_tag as svc_add_tag,
    get_tag_by_id as svc_get_tag_by_id,
    get_tag_by_name as svc_get_tag_by_name,
    update_tag as svc_update_tag,
    delete_tag as svc_delete_tag,
)
from src.core.auth import login_required
from src.core.tagForm import TagForm


bp = Blueprint("tags", __name__, url_prefix="/etiquetas")


@bp.get("/")
@login_required
def index():
    """Muestra el listado paginado de etiquetas con filtros opcionales."""
    page = request.args.get("page", 1, type=int)
    per_page = 25

    filtros = request.args.to_dict()
    filtros.pop("page", None)
    filtros.pop("per_page", None)

    pagination = svc_list_tags(filtros).paginate(page=page, per_page=per_page)

    return (
        render_template(
            "tags/tags_table.html",
            items=pagination.items,
            pagination=pagination,
            filtros=filtros,
        ),
        200,
    )


@bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def add_tag():
    """Crea una nueva etiqueta o renderiza el formulario."""
    form = TagForm()

    if form.validate_on_submit():
        nombre = form.name.data.strip()
        # Validación adicional: existencia en BD
        is_existing = svc_get_tag_by_name(nombre.lower())
        if is_existing:
            flash("Ya existe una etiqueta con ese nombre.", "error")
            return redirect(url_for("tags.add_tag"))

        # Crear la etiqueta
        svc_add_tag({"nombre": nombre})
        flash("Etiqueta creada exitosamente.", "success")
        return redirect(url_for("tags.index"))

    # Si GET o si hay errores, renderizar el formulario
    return render_template("tags/add_tag.html", form=form)


@bp.route("/editar/<int:tag_id>", methods=["GET", "POST"])
@login_required
def edit_tag(tag_id):
    """Edita una etiqueta existente o renderiza el formulario con los datos actuales."""
    tag = svc_get_tag_by_id(tag_id)
    if not tag:
        flash("Etiqueta no encontrada.", "error")
        return redirect(url_for("tags.index"))
    form = TagForm(obj=tag)
    if form.validate_on_submit():
        nombre = form.name.data.strip()
        # Validación adicional: existencia en BD (excluyendo la actual)
        is_existing = svc_get_tag_by_name(nombre.lower())
        if is_existing and is_existing.id != tag.id:
            flash("Ya existe una etiqueta con ese nombre.", "error")
            return redirect(url_for("tags.edit_tag", tag_id=tag.id))

        # Actualizar la etiqueta
        svc_update_tag(tag_id, {"nombre": nombre})
        flash("Etiqueta actualizada exitosamente.", "success")
        return redirect(url_for("tags.index"))
    return render_template("tags/edit_tag.html", form=form, tag=tag)


@bp.post("/eliminar/<int:tag_id>")
@login_required
def delete_tag(tag_id):
    """Elimina una etiqueta si no está asociada a ningún sitio."""
    try:
        svc_delete_tag(tag_id)
        flash("Etiqueta eliminada exitosamente.", "success")
    except ValueError as e:
        flash(str(e), "error")
    return redirect(url_for("tags.index"))
