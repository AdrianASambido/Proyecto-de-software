from flask import render_template

def page_not_found(error):
    return render_template("errores/404.html"), 404

def internal_error(error):
    return render_template("errores/500.html"), 500

