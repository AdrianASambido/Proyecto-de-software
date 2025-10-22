from minio import Minio

class Storage:
    def __init__(self, app=None):
        self._cliente = None

        if app is not None:
            self.__init__app(app)

    def init_app(self, app):
        self._cliente = Minio(
            #acá 
        app.Config["MINIO_SERVER"],
        SECRET_KEY = app.config["MINIO_access_key"],
        

        )