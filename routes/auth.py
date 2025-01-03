from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

jwt = JWTManager()

auth_bp = Blueprint('auth', __name__)

users_db = {
    'admin': 'password'  
}

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login route to authenticate and generate JWT token."""
    username = request.json.get('username')
    password = request.json.get('password')
    
    if users_db.get(username) == password:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    """A protected route that requires a valid JWT token."""
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
