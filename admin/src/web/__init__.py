from flask import Flask, render_template, abort 
from src.web.config import config

def create_app(env="development", static_folder="../../static"): #../../static
    app = Flask(__name__, static_folder=static_folder)
    app.config.from_object(config[env])


    @app.route("/")
    def home():
        return render_template("home.html")
    
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
    
    return app
