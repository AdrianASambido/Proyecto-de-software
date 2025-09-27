from flask import Blueprint
from flask import render_template, request, redirect, url_for

bp = Blueprint("login", __name__, url_prefix=("/auth"))

@bp.get("/")
def login():
    return render_template("login/login_usuario.html"), 200


def logout():
    pass

def authenticate():
    pass