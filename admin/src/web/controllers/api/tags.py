from flask import jsonify, request
from . import api_bp
from src.core.services.tags import list_tags

@api_bp.get("/tags")
def get_tags():
    """
    Endpoint público para obtener la lista de tags disponibles.
    """
    filtros = {}
    busqueda = request.args.get("busqueda")
    if busqueda:
        filtros["busqueda"] = busqueda
    
    query = list_tags(filtros)
    tags = query.all()
    
    data = [{"id": tag.id, "name": tag.name} for tag in tags]
    
    return jsonify({"data": data}), 200


