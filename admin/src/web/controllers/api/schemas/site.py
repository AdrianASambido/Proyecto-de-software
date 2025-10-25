from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from src.core.Entities.site import Site 

class SiteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Site  
        load_instance = True
        include_relationships = True
        include_fk = False
        fields = (
            "id",
            "nombre",
            "descripcion_breve",
            "descripcion_completa",
            "ciudad",
            "provincia",
            "categoria",
            "estado_conservacion",
            "inauguracion",
            "latitud",
            "longitud",
            "tags",
        )


    tags = fields.Method("get_tags")

    latitud = fields.Method("get_latitud")
    longitud = fields.Method("get_longitud")

    def get_latitud(self, obj):
        return obj.latitud

    def get_longitud(self, obj):
        return obj.longitud

    def get_tags(self, obj):
        
        return [tag.name for tag in obj.tags] if obj.tags else []