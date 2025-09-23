from flask import render_template, Blueprint, request, redirect, url_for    
from src.core import board_tags

bp = Blueprint("tags", __name__, url_prefix="/tags")

@bp.get("/")
def index():
    tags = board_tags.get_tags()

    return render_template("tags/tags_table.html", tags=tags), 200


@bp.get("/nuevo")
def add_form():
    return render_template("tags/add_tag.html"), 200


@bp.post("/create")
def add_tag():
    tag_data = dict(request.form)
    board_tags.add_tag(tag_data)
    
    return redirect(url_for("tags.index"))

@bp.get("/editar/<int:tag_id>")
def edit_form(tag_id):
    tag = board_tags.get_tag_by_id(tag_id)
    return render_template("tags/edit_tag.html", tag=tag)

@bp.post("/editar/<int:tag_id>")
def edit_tag(tag_id):
    tag_data = dict(request.form)
    board_tags.update_tag(tag_id, tag_data)
    
    return redirect(url_for("tags.index"))


@bp.post("/eliminar/<int:tag_id>")
def delete_tag(tag_id):
    board_tags.delete_tag(tag_id)
    return redirect(url_for("tags.index"))
