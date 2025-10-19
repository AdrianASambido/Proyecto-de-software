from flask import jsonify,request
from . import api_bp


@api_bp.get("sites/<int:site_id>/reviews")
def get_reviews_for_site(site_id):
    pass

@api_bp.post("sites/<int:site_id>/reviews")
def add_review_to_site(site_id):
    pass

@api_bp.get("sites/<int:site_id>/reviews/<int:review_id>")
def get_review_by_id(site_id, review_id):
    pass


@api_bp.delete("sites/<int:site_id>/reviews/<int:review_id>")
def delete_review(site_id, review_id):
    pass