"""
Archivo de configuracion para los distintos ambientes
"""

import os


class Config:
    TESTING = False
    SECRET_KEY = os.getenv("COMMON_SECRET", "dev-secret-change-me")
    SESSION_TYPE = os.getenv("COMMON_SESSION_TYPE", "filesystem")
    DEBUG_VARIABLE = os.getenv("COMMON_DEBUG")


class ProductionConfig(Config):
    MINIO_SERVER = os.getenv("MINIO_SERVER")
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
    MINIO_SECURE = True
    MINIO_BUCKET = "grupo01"

    CORS_ORIGINS=[
        "https://grupo01.proyecto2025.linti.unlp.edu.ar/"
    ]
    DB_USER = os.getenv("DATABASE_USERNAME")
    DB_PASSWORD = os.getenv("DATABASE_PASSWORD")
    DB_HOST = os.getenv("DATABASE_HOST")
    DB_PORT = os.getenv("DATABASE_PORT")
    DB_NAME = os.getenv("DATABASE_NAME")

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": int(os.getenv("SQLALCHEMY_POOL_RECYCLE", 1800)),
        "pool_size": int(os.getenv("SQLALCHEMY_POOL_SIZE", 5)),
        "max_overflow": int(os.getenv("SQLALCHEMY_MAX_OVERFLOW", 10)),
        "pool_timeout": int(os.getenv("SQLALCHEMY_POOL_TIMEOUT", 30)),
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = (
        os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", "True").lower() == "true"
    )
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        if all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME])
        else None
    )


class DevelopmentConfig(Config):
    """
    Configuración para desarrollo
    """
    MINIO_SERVER = "localhost:9000"
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "admin")
    MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "admin123")
    MINIO_SECURE = False
    MINIO_BUCKET = "grupo01"

    CORS_ORIGINS=[
        "*"
    ]
    DB_USER = os.getenv("GRUPO01_DATABASE_USERNAME", "postgres")
    DB_PASSWORD = os.getenv("GRUPO01_DATABASE_PASSWORD", "Sacsayhuaman03")
    DB_HOST = os.getenv("GRUPO01_DATABASE_HOST", "localhost")
    DB_PORT = os.getenv("GRUPO01_DATABASE_PORT", "5432")
    DB_NAME = os.getenv("GRUPO01_DATABASE_NAME", "postgres")

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": int(os.getenv("SQLALCHEMY_POOL_RECYCLE", 1800)),
        "pool_size": int(os.getenv("SQLALCHEMY_POOL_SIZE", 5)),
        "max_overflow": int(os.getenv("SQLALCHEMY_MAX_OVERFLOW", 10)),
        "pool_timeout": int(os.getenv("SQLALCHEMY_POOL_TIMEOUT", 30)),
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = (
        os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", "True").lower() == "true"
    )
    SQLALCHEMY_DATABASE_URI = os.getenv("GRUPO01_DATABASE_URL") or (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


class TestingConfig(Config):
    TESTING = True
    DB_USER=os.getenv("GRUPO01_DATABASE_USERNAME", "postgres")
    DB_PASSWORD=os.getenv("GRUPO01_DATABASE_PASSWORD", "Sacsayhuaman03")
    DB_HOST=os.getenv("GRUPO01_DATABASE_HOST", "localhost")
    DB_PORT=os.getenv("GRUPO01_DATABASE_PORT", "5432")
    DB_NAME=os.getenv("GRUPO01_DATABASE_NAME", "postgres")

    DB_USER = os.getenv("GRUPO01_DATABASE_USERNAME", "postgres")
    DB_PASSWORD = os.getenv("GRUPO01_DATABASE_PASSWORD", "Sacsayhuaman03")
    DB_HOST = os.getenv("GRUPO01_DATABASE_HOST", "localhost")
    DB_PORT = os.getenv("GRUPO01_DATABASE_PORT", "5432")
    DB_NAME = os.getenv("GRUPO01_DATABASE_NAME", "postgres")

    SQLALCHEMY_TRACK_MODIFICATIONS = (
        os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", "True").lower() == "true"
    )
    SQLALCHEMY_DATABASE_URI = os.getenv("GRUPO01_DATABASE_URL") or (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
