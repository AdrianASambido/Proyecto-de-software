from flask import Flask, render_template, abort 


def create_app(static_folder="static"):
    app = Flask(__name__, static_folder=static_folder)

    @app.route("/")
    def home():
        return render_template("home.html")

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('/errores/404.html'), 404
    
    @app.errorhandler(500)
    def page_not_found(error):
        return render_template('/errores/500.html'), 500

    @app.route("/error-500")
    def throw_500_error_for_test():
        abort(500)
        return render_template("throw_500_error_for_test.html")
    
    return app
