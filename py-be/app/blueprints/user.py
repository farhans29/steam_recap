#Import Library
from flask import Blueprint, jsonify, request
from flasgger import swag_from
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt


#Import Dependencies
from app import db
from app.models.user import User

user_bp = Blueprint('user_bp', __name__)

# GET USERS
@user_bp.route('/user/get', methods=['GET'])
@swag_from({
    'parameters': [
        {
            'in': 'header',
            'name': 'Authorization',
            'type': 'string',
            'required': True,
            'description': 'JWT token. Format: Bearer <access_token>'
        }
    ],
    'responses' : {
        200: {
            'description' : 'List of users',
            'examples' : {
                'application/json' : [
                    {
                        'user_id' : 1,
                        'user_name': 'John Doe',
                        'user_email' : 'john@email.com'
                    },
                    {
                        'user_id' : 2,
                        'user_name': 'Jane Doe',
                        'user_email' : 'jane@email.com', 
                    }
                ]
            }
        }
        
    }
})

@jwt_required()
def get_users():
    """
    Get all user.
    """
    current_user_id = get_jwt_identity()
    if current_user_id is None:
        return jsonify({'error': 'Invalid access token'}),401
    
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


# ADD USER
@user_bp.route('/user/create', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'in': 'body',
            'name': 'user',
            'description': 'User object',
            'schema': {
                'type': 'object',
                'properties': {
                    'user_name': {'type': 'string'},
                    'user_email': {'type': 'string'},
                    'user_password': {'type': 'string'}
                },
                'required': ['user_name', 'user_email', 'user_password']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'User created successfully',
            'examples': {
                'application/json': {
                    'user_id': 1,
                    'user_name': 'John Doe',
                    'user_email': 'john@example.com'
                }
            }
        }
    }
})
def create_user():
    """
    Add User.
    """
    data = request.get_json()
    new_user = User(user_name=data['user_name'], user_email=data['user_email'])
    new_user.set_password(data['user_password'])

    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

# DELETE USER
@user_bp.route('/user/delete/<string:user_id>', methods=['DELETE'])
@swag_from({
    'parameters': [
        {
            'in': 'header',
            'name': 'Authorization',
            'type': 'string',
            'required': True,
            'description': 'JWT token. Format: Bearer <access_token>'
        },
        {
            'in': 'path',
            'name': 'user_id',
            'description': 'ID of the user to delete',
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

@jwt_required
def delete_user(user_id):
    """
    Delete a user by ID.
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return '',204

# UPDATE USER
@user_bp.route('/user/update/<string:user_id>', methods=['PUT'])
@swag_from({
    'parameters': [
        {
            'in': 'header',
            'name': 'Authorization',
            'type': 'string',
            'required': True,
            'description': 'JWT token. Format: Bearer <access_token>',
        },
        {
            'in': 'path',
            'name': 'user_id',
            'description': 'ID of the user to edit',
            'required': True,
            'type': 'string'
        },
        {
            'in': 'body',
            'name': 'user_data',
            'description': 'Updated user data',
            'schema': {
                'type': 'object',
                'properties': {
                    'user_name': {'type': 'string'},
                    'user_email': {'type': 'string'},
                    'user_password': {'type': 'string'}
                }
            }
        },

    ],
    'responses': {
        200: {
            'description': 'User edited successfully'
        },
        404: {
            'description': 'User not found'
        }
    }
})
def edit_user(user_id):
    """
    Edit user data by ID.
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    if 'user_name' in data:
        user.user_name = data['user_name']
    if 'user_email' in data:
        user.email = data['user_email']
    if 'user_password' in data:
        user.set_password(data['user_password'])

    db.session.commit()
    return '', 200

# LOGIN USER
@user_bp.route('/user/login', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'in': 'body',
            'name': 'login_data',
            'description': 'Login credentials',
            'schema': {
                'type': 'object',
                'properties': {
                    'user_email': {'type': 'string'},
                    'user_password': {'type': 'string'}
                },
                'required': ['user_email', 'user_password']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Login successful',
            'examples': {
                'application/json': {
                    'access_token': 'jwt_access_token'
                }
            }
        },
        401: {
            'description': 'Invalid credentials'
        }
    }
})
def login():
    """
    Log in with email and password.
    """
    data = request.get_json()
    email = data.get('user_email', None)
    password = data.get('user_password', None)

    if not email or not password :
        return jsonify({'error': 'Email and password are required'}), 400
    
    user = User.query.filter_by(user_email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=user.user_id)
    return jsonify({'access_token': access_token}), 200

# LOGOUT USER
@user_bp.route('/user/logout', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'in': 'header',
            'name': 'Authorization',
            'type': 'string',
            'required': True,
            'description': 'JWT token. Format: Bearer <access_token>'
        }
    ],
    'responses': {
        200: {
            'description': 'Successfully logged out',
            'examples': {
                'application/json': {
                    'message': 'Successfully logged out'
                }
            }
        },
        401: {
            'description': 'Unauthorized - Missing or invalid token',
            'examples': {
                'application/json': {
                    'msg': 'Missing Authorization Header'
                }
            }
        }
    }
})

@jwt_required()
def logout():
    """
    Log out the current user.
    """

    jwt = get_jwt()
    jwt['exp'] = 0

    return jsonify({'message': 'Successfully logged out'}), 200


# UPDATE GENRE_ID ON USER TABLE