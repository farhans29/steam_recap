#Import Library
import ast
import json
from flask import Blueprint, jsonify, request
from flasgger import swag_from
from datetime import datetime

#Import Dependencies
from app import db
from app.models.genre import Genre


genre_bp = Blueprint('genre_bp', __name__)

# GET GENRES
@genre_bp.route('/genre/get', methods=['GET'])
@swag_from({

    'responses' : {
        200: {
            'description' : 'List of genres',
            'examples' : {
                'application/json' : [
                    {
                        'genre_id' : '101',
                        'genre_titles': 'John Doe',
                        'user_id' : '1'
                    },
                    {
                        'genre_id' : '102',
                        'genre_titles': 'John Doe',
                        'user_id' : '2'
                    }
                ]
            }
        }
        
    }
})
def get_genres():
    """
    Get all genres based on users.
    """
    genres = Genre.query.all()
    return jsonify([g.to_dict() for g in genres])
    
# CREATE GENRES
@genre_bp.route('/genre/create', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'in': 'body',
            'name': 'user',
            'description': 'User object',
            'schema': {
                'type': 'object',
                'properties': {
                    'genre_titles': {'type': 'string'},
                    'user_id': {'type': 'string'}
                },
                'required': ['genre_titles', 'user_id']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Genre created successfully',
            'examples': {
                'application/json': {
                        'genre_id' : '101',
                        'genre_titles': 'John Doe',
                        'user_id' : '1'
                    }
            }
        }
    }
})
def create_genres():
    """
    Add Genres.
    """
    data = request.get_json()
    genre_titles = data['genre_titles']
    if isinstance(genre_titles, list):
        serialized_titles = json.dumps(genre_titles)
    else:
        serialized_titles = json.dumps(ast.literal_eval(genre_titles))
        
    new_genres = Genre(genre_titles=serialized_titles, user_id=data['user_id'])
    
    db.session.add(new_genres)
    db.session.commit()
    return jsonify(new_genres.to_dict()), 201

# UPDATE GENRES BY GENRE_ID
@genre_bp.route('/genre/genreId/<string:genre_id>', methods=['PUT'])
@swag_from({
    'parameters': [
        {
            'in': 'path',
            'name': 'genre_id',
            'description': 'ID of the genre to edit',
            'required': True,
            'type': 'string'
        },
        {
            'in': 'body',
            'name': 'genre_data',
            'description': 'Updated genre data',
            'schema': {
                'type': 'object',
                'properties': {
                    'genre_titles': {'type': 'string'},
                }
            }
        },
        
    ],
    'responses': {
        200: {
            'description':'Genre deleted successfully'
        },
        404: {
            'description':'Genre not found'
        }
    }
})
def edit_genres_by_genreId(genre_id):
    """
    Update genre by genre_id
    """
    genre = Genre.query.get(genre_id)
    if not genre:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    if 'genre_titles' in data:
        serialized_titles = json.dumps(data['genre_titles'])  # Serialize the array
        genre.genre_titles = serialized_titles
    if 'user_id' in data:
        genre.user_id = data['user_id']
    
    db.session.commit()
    return '', 200

# DELETE GENRES BY GENRE_ID
@genre_bp.route('/genre/delete/<string:genre_id>', methods=['DELETE'])
@swag_from({
    'parameters': [
        {
            'in': 'path',
            'name': 'genre_id',
            'description': 'ID of the genre to delete',
            'required': True,
            'type': 'string'
        }
        
    ],
    'responses': {
        204: {  
            'description': 'User deleted successfully'
        },
        404: {
            'description': 'User not found'
        }
    }
})
def delete_genres(genre_id):
    """
    Delete genres by genre_id
    """
    genre = Genre.query.get(genre_id)
    if not genre:
        return jsonify({'error':'User not found'}), 404
    db.session.delete(genre)
    db.session.commit()
    return '', 204


# UPDATE GENRES BY USER_ID
@genre_bp.route('/genre/userId/<string:user_id>', methods=['PUT'])
@swag_from({
    'parameters': [
        {
            'in': 'path',
            'name': 'user_id',
            'description': 'ID of the user to edit the genre',
            'required': True,
            'type': 'string'
        },
        {
            'in': 'body',
            'name': 'genre_data',
            'description': 'Updated genre data',
            'schema': {
                'type': 'object',
                'properties': {
                    'genre_titles': {'type': 'string'},
                }
            }
        },
        
    ],
    'responses': {
        200: {
            'description':'Genre deleted successfully'
        },
        404: {
            'description':'Genre not found'
        }
    }
})
def edit_genres_by_userId(user_id):
    """
    Update genre by user_id
    """
    genres = Genre.query.filter_by(user_id=user_id).all()
    if not genre:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    if 'genre_titles' in data:
        serialized_titles = json.dumps(data['genre_titles'])  # Serialize the array
        for genre in genres:
            genre.genre_titles = serialized_titles
    if 'genre_id' in data:
        for genre in genres:
            genre.genre_id = data['genre_id']
    
    db.session.commit()
    return '', 200
