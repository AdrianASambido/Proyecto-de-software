from flask import render_template, Blueprint, request, redirect, url_for, flash
from src.core.services.tags import (
    list_tags as svc_list_tags,
    add_tag as svc_add_tag,
    get_tag_by_id as svc_get_tag_by_id,
    get_tag_by_name as svc_get_tag_by_name,
    update_tag as svc_update_tag,
    delete_tag as svc_delete_tag,
)

bp = Blueprint("tags", __name__, url_prefix="/tags")

@bp.get("/")
def index():
    filtros = request.args.to_dict()
    tags = svc_list_tags(filtros)
    return render_template("tags/tags_table.html", items=tags), 200


@bp.get("/nuevo")
def add_tag():
    return render_template("tags/add_tag.html"), 200

@bp.get("/editar/<int:tag_id>")
def edit_tag(tag_id):
    tag = svc_get_tag_by_id(tag_id)
    return render_template("tags/edit_tag.html", tag=tag)


@bp.post("/create")
def add_tag_handler():
    tag_data = dict(request.form)
    isExistingTag = svc_get_tag_by_name(tag_data.get("nombre").lower())
    
    if isExistingTag:
        flash("Ya existe una etiqueta con ese nombre.", "error")
        return redirect(url_for("tags.add_tag"))

    svc_add_tag(tag_data)
    flash("Etiqueta creada exitosamente.", "success")
    return redirect(url_for("tags.index"))

@bp.post("/editar/<int:tag_id>")
def edit_tag_handler(tag_id):
    tag_data = dict(request.form)
    svc_update_tag(tag_id, tag_data)
    flash("Etiqueta modificada exitosamente.", "success")
    return redirect(url_for("tags.index"))

@bp.post("/eliminar/<int:tag_id>")
def delete_tag_handler(tag_id):
    try:
        svc_delete_tag(tag_id)
        flash("Etiqueta eliminada exitosamente.", "success")
    except ValueError as e:
        flash(str(e), "error")
    return redirect(url_for("tags.index"))
