from flask import Blueprint
from flask_restx import Api, Resource, Namespace, fields
from app.database import db
from app.auth import views, schemas

auth_bp = Blueprint('auth', __name__)
api = Namespace('auth', description='Authentication operations')

# Models
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

response_model = api.model('Response', {
    'message': fields.String,
    'status_code': fields.Integer,
    'data': fields.Raw
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.response(200, 'Success', response_model)
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Login with email and password to get JWT token"""
        data = api.payload
        return views.login(schemas.LoginRequest(**data), db.session)