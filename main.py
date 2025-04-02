from flask import Flask, jsonify, request
from flask_restx import Api
from flask_jwt_extended import JWTManager
from app.database import db
from app.user_types.routes import api as user_types_ns
from app.user_roles.routes import api as user_roles_ns
from app.users.routes import api as users_ns
from app.auth.routes import api as auth_ns
import os
from datetime import timedelta

# Import all models to ensure they are registered with SQLAlchemy
from app.user_types.models import UserTypeDB
from app.user_roles.models import UserRoleDB
from app.users.models import UserDB, user_roles

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Sabit bir key kullanalım test için
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'  # Bearer prefix required
app.config['JWT_AUTH_HEADER_PREFIX'] = 'Bearer'


# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)

# Debug middleware
@app.before_request
def log_request_info():
    auth_header = request.headers.get('Authorization')
    print('Auth Header:', auth_header)
    if auth_header:
        print('Token:', auth_header.replace('Bearer ', ''))

# JWT error handlers
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'message': 'Token formatı hatalı. "Bearer <token>" formatında olmalı.',
        'error': 'invalid_token'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'message': 'Authorization header eksik veya hatalı.',
        'error': 'authorization_required'
    }), 401

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'message': 'Token süresi dolmuş. Lütfen yeniden login olun.',
        'error': 'token_expired'
    }), 401

# Initialize API with authorizations
authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "JWT Authorization header using the Bearer scheme. Example: **'Bearer <JWT>'**"
    }
}

api = Api(
    app,
    version='1.0',
    title='My API',
    description='Flask RESTX with JWT',
    authorizations=authorizations,
    security='Bearer'  # Global olarak JWT koruması uygular
)

# Add namespaces
api.add_namespace(auth_ns)
api.add_namespace(user_types_ns)
api.add_namespace(user_roles_ns)
api.add_namespace(users_ns)

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)