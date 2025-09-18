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