from flask import render_template, Blueprint, request, redirect, url_for
from src.core.services.tags import (
    list_tags as svc_list_tags,
    add_tag as svc_add_tag,
    get_tag_by_id as svc_get_tag_by_id,
    update_tag as svc_update_tag,
    delete_tag as svc_delete_tag,
)

bp = Blueprint("tags", __name__, url_prefix="/tags")

@bp.get("/")
def index():
    tags = svc_list_tags()
    return render_template("tags/tags_table.html", items=tags), 200


@bp.get("/nuevo")
def add_tag():
    return render_template("tags/add_tag.html"), 200


@bp.post("/create")
def add_tag_handler():
    tag_data = dict(request.form)
    svc_add_tag(tag_data)
    return redirect(url_for("tags.index"))


@bp.get("/editar/<int:tag_id>")
def edit_tag(tag_id):
    tag = svc_get_tag_by_id(tag_id)
    return render_template("tags/edit_tag.html", tag=tag)


@bp.post("/editar/<int:tag_id>")
def edit_tag_handler(tag_id):
    tag_data = dict(request.form)
    svc_update_tag(tag_id, tag_data)
    return redirect(url_for("tags.index"))

@bp.post("/eliminar/<int:tag_id>")
def delete_tag_handler(tag_id):
    svc_delete_tag(tag_id)
    return redirect(url_for("tags.index"))
