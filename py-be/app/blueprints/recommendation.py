#Import Library
import ast
import json
from flask import Blueprint, jsonify, request
from flasgger import swag_from
from datetime import datetime

#Import Dependencies
from app import db
from app.models.recommendation import Recommendation

recommendation_bp = Blueprint('recommendation_bp', __name__)

# GET RECOMMENDATION
@recommendation_bp.route('/recommendation/get', methods=['GET'])
@swag_from({

})
def get_recommendation():
    """
    Get recommendation for users.
    """
    recommendations = Recommendation.query.all()
    return jsonify([r.to_dict() for r in recommendations ])

# CREATE RECOMMENDATION
@recommendation_bp.route('/recommendation/create', methods=['POST'])
@swag_from({

})
def create_recommendation():
    """
    Create new recommendation for user
    """
    data = request.get_json()
    recommendation_titles = data['recommendation_titles']
    if isinstance(recommendation_titles, list):
        serialized_titles = json.dumps(recommendation_titles)
    else:
        serialized_titles = json.dumps(ast.literal_eval(recommendation_titles))

    new_recommendation = Recommendation(recommendation_titles=serialized_titles, user_id=data['user_id'])

    db.session.add(new_recommendation)
    db.session.commit()
    return jsonify(new_recommendation.to_dict()), 201

# UPDATE RECOMMENDATION

# DELETE RECOMMENDATION