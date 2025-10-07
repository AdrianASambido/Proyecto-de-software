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
from flask_session import Session
from src.core.auth import login_required
from src.core.auth import has_permission,is_system_admin_user
from src.core.services.feature_flags import is_admin_maintenance_mode,get_admin_maintenance_message

from datetime import timedelta

sess=Session()

def create_app(env="development", static_folder="../../static"):  # ../../static

    app = Flask(__name__, static_folder=static_folder)
    app.config.from_object(config[env])
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=1)
    database.init_app(app)
    sess.init_app(app)
   

    # Middleware para verificar flags de mantenimiento
    @app.before_request
    def check_maintenance_mode():
        # Rutas que siempre están disponibles (login y feature flags para system admin)
        exempt_routes = [
            "login.login",
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

     

    @app.route("/")
    def login():
       
        return redirect(url_for("login.login"))
    


    
    @app.route("/home")
    @login_required
    def home():
        return render_template("home.html"), 200

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
    # helpers para jinja
    app.jinja_env.globals["has_permission"] = has_permission
    app.jinja_env.globals["is_system_admin_user"] = is_system_admin_user  
    app.jinja_env.globals["is_admin_maintenance_mode"] = is_admin_maintenance_mode
    app.jinja_env.globals["get_admin_maintenance_message"] = get_admin_maintenance_message  

     
    @app.context_processor
    def inject_user_flags():
        return dict(is_system_admin_user=is_system_admin_user())


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
