from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from src.core.Entities.site import Site 
from src.core.services.sites import calculate_valoration,calculate_review_count

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
            "cover_url",
            "valoracion_promedio",
            "cantidad_resenias",
        )

    tags = fields.Method("get_tags")
    latitud = fields.Method("get_latitud")
    longitud = fields.Method("get_longitud")
    cover_url = fields.Method("get_cover_url")
    valoracion_promedio = fields.Method("get_valoracion_promedio")
    cantidad_resenias=fields.Method("get_cantidad_resenias")


    def get_cantidad_resenias(self, obj):
        return calculate_review_count(obj.id)

    def get_valoracion_promedio(self, obj):
        return calculate_valoration(obj.id)

    def get_latitud(self, obj):
        return obj.latitud

    def get_longitud(self, obj):
        return obj.longitud

    def get_tags(self, obj):
        return [tag.name for tag in obj.tags] if obj.tags else []

    def get_cover_url(self, obj):

        if hasattr(obj, "_cover_url"):
            return obj._cover_url
   
        return getattr(obj, "cover_url", None)
