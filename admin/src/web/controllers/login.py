from flask import Blueprint
from flask import render_template, request
from src.core import board_usuarios

bp = Blueprint("users", __name__, url_prefix=("/auth"))

def login():
    pass

def logout():
    pass

def authenticate():
    pass