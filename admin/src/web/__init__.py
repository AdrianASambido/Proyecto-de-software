from flask import Flask, render_template, abort, redirect, url_for, request
from src.web.config import config

from src.core import database, seeds
from src.core.services.feature_flags import (
    is_admin_maintenance_mode,
    get_admin_maintenance_message,
    is_portal_maintenance_mode,
    get_portal_maintenance_message,
)

# ACA controladores
from src.web.controllers.users import bp as users_bp
from src.web.controllers.sites import bp as sites_bp
from src.web.controllers.tags import bp as tags_bp
from src.web.controllers.feature_flags import bp as feature_flags_bp
from src.web.controllers.login import bp as login_bp
from src.web.controllers.sites_history import bp as sites_history_bp



def create_app(env="development", static_folder="../../static"):  # ../../static

    app = Flask(__name__, static_folder=static_folder)
    app.config.from_object(config[env])

    database.init_app(app)
    # Middleware para verificar flags de mantenimiento
    @app.before_request
    def check_maintenance_mode():
        # Rutas que siempre están disponibles (login y feature flags para system admin)
        exempt_routes = [
            "login",
            "feature_flags.index",
            "feature_flags.toggle_flag",
            "feature_flags.get_flags_status",
        ]

        # Si es una ruta de administración y está en modo mantenimiento
        if (
            request.endpoint
            and request.endpoint.startswith("sites")
            and is_admin_maintenance_mode()
        ):
            # Permitir acceso a feature flags para system admin
            if request.endpoint not in exempt_routes:
                message = get_admin_maintenance_message()
                return (
                    render_template(
                        "errores/maintenance.html",
                        message=message,
                        title="Sistema en Mantenimiento",
                    ),
                    503,
                )

        # Si es una ruta del portal y está en modo mantenimiento
        if request.endpoint == "home" and is_portal_maintenance_mode():
            message = get_portal_maintenance_message()
            return (
                render_template(
                    "errores/maintenance.html",
                    message=message,
                    title="Portal en Mantenimiento",
                ),
                503,
            )

    @app.route("/")
    def home():
        return render_template("home.html"), 200


    @app.route("/tabla")
    def tabla():
        return render_template("tables_base.html"), 200

    @app.errorhandler(401)
    def unauthorizedError(error):
        return render_template("errores/401.html"), 401

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errores/404.html"), 404

    @app.errorhandler(500)
    def internalError(error):
        return render_template("errores/500.html"), 500

    @app.route("/error-401")
    def throw_401_error_for_test():
        abort(401)

    @app.route("/error-500")
    def throw_500_error_for_test():
        abort(500)
        return render_template("throw_500_error_for_test.html")

    # definir todos los blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(sites_bp)
    app.register_blueprint(sites_history_bp)
    app.register_blueprint(tags_bp)
    app.register_blueprint(feature_flags_bp)
    app.register_blueprint(login_bp)
    
    #comandos para el CLI
    @app.cli.command(name="resetdb")
    def resetdb():
        database.reset_db()

    @app.cli.command(name="seeddb")#correrlo como "flask --app src.web seeddb"
    def seeddb():
        seeds.seeds_db()


    return app
