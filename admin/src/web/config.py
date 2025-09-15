"""
Archivo de configuracion para los distintos ambientes
"""

class Config:
    TESTING=False
    SECRET_KEY=""
    SESSION_TYPE="filesystem"

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    pass

class TestingConfig(Config):
    TESTING=True


config={
    "development":DevelopmentConfig,
    "production":ProductionConfig,
    "testing":TestingConfig,

}