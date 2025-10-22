
from flask import jsonify,request
from . import api_bp


@api_bp.put("sites/<int:site_id>/favorite")
def favorite():
    pass
    
