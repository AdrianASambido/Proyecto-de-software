from flask_sqlalchemy import SQLAlchemy
# esto se ejecuta e la terminal con "flask resetdb"
db = SQLAlchemy()

def init_app(app):
    db.init_app(app)

def config_db(app):
    @app.teardown_request
    def close_session(exception=None):
        db.session.close()

def reset_db():
    print("\n\n==== BORRANDO BASE DE DATOS ====")
    db.drop_all()
    print("\n==== CREANDO BASE DE DATOS ====")
    db.create_all()
    print("\n==== RESET LISTO ====\n\n")