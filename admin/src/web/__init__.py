from flask import Flask, render_template, abort, redirect, url_for
from src.web.config import config
from src.core import database, seeds

# ACA controladores
from src.web.controllers.sites import bp as sites_bp
from src.web.controllers.tags import bp as tags_bp

def create_app(env="development", static_folder="../../static"): #../../static
    app = Flask(__name__, static_folder=static_folder)
    app.config.from_object(config[env])

    database.init_app(app)

    @app.route("/")
    def home():
        return render_template("home.html"), 200
    
    @app.route("/tabla")
    def tabla():
        return render_template("tables_base.html"), 200
    
    @app.route("/login")
    def login():
        return render_template("/login/login_usuario.html"), 200
    
    
    @app.errorhandler(401)
    def unauthorizedError(error):
        return render_template('errores/401.html'), 401

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errores/404.html'), 404
    
    @app.errorhandler(500)
    def internalError(error):
        return render_template('errores/500.html'), 500

    @app.route("/error-401")
    def throw_401_error_for_test():
        abort(401)

    @app.route("/error-500")
    def throw_500_error_for_test():
        abort(500)
        return render_template("throw_500_error_for_test.html")
    

    # definir todos los blueprints
    app.register_blueprint(sites_bp)
    app.register_blueprint(tags_bp)
    
    
    #comandos para el CLI
    @app.cli.command(name="resetdb")
    def resetdb():
        database.reset_db()

    @app.cli.command(name="seeddb")
    def seeddb():
        seeds.seeds_db()

    return app
