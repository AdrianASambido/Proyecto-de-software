from flask import Flask, render_template, abort, redirect, url_for, request
from src.web.config import config
from src.web.storage import storage
from src.core import database, seeds
from src.core.services.feature_flags import (
    is_admin_maintenance_mode,
    get_admin_maintenance_message,
    is_portal_maintenance_mode,
    get_portal_maintenance_message,
)
from flask_cors import CORS

# ACA controladores
from src.web.controllers.users import bp as users_bp
from src.web.controllers.sites import bp as sites_bp
from src.web.controllers.tags import bp as tags_bp
from src.web.controllers.feature_flags import bp as feature_flags_bp
from src.web.controllers.login import bp as login_bp
from src.web.controllers.api import api_bp
from src.web.controllers.sites_history import bp as sites_history_bp
from src.web.controllers.reviews import bp as reviews_bp
from flask_session import Session
from src.core.auth import login_required
from src.core.auth import has_permission,is_system_admin_user
from src.core.services.feature_flags import is_admin_maintenance_mode,get_admin_maintenance_message
from src.web.handlers import errors
from datetime import timedelta

sess=Session()

def create_app(env="development", static_folder="../../static"):  # ../../static
    app = Flask(__name__, static_folder=static_folder)
    app.config.from_object(config[env])
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=1)
    #initialize database, 
    database.init_app(app)
    database.config_db(app)
    sess.init_app(app)
    storage.init_app(app)
    CORS(
        app,
        resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}},
        supports_credentials=True
    )
    # Middleware para verificar flags de mantenimiento
    @app.before_request # se ejecuta antes de cada solicitud HTTP
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
            # Bloquea sitios, etiquetas usuarios
            and (request.endpoint.startswith("sites") or request.endpoint.startswith("tags") or request.endpoint.startswith("users"))
            and is_admin_maintenance_mode() and not is_system_admin_user
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
                    503, # código HTTP de Service Unavailable
                )


    @app.route("/")
    def login():
        return redirect(url_for("login.login"))
    
    @app.route("/home")
    @login_required
    def home():
        return render_template("home.html"), 200


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
    app.register_blueprint(reviews_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(feature_flags_bp)
    app.register_blueprint(login_bp)

    # registrar handlers de errores
    app.register_error_handler(404, errors.not_found)
    app.register_error_handler(500, errors.internal_error)
    
    
    #comandos para el CLI
    @app.cli.command(name="resetdb")
    def resetdb():
        database.reset_db()

    @app.cli.command(name="seeddb")#correrlo como "flask --app src.web seeddb"
    def seeddb():
        seeds.seeds_db()


    return app
