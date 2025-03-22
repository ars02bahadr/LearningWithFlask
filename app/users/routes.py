from flask import Blueprint
from flask_restx import Api, Resource, Namespace, fields
from app.database import db
from app.users import views, schemas
from werkzeug.datastructures import FileStorage
from flask_jwt_extended import jwt_required, get_jwt_identity
import os

users_bp = Blueprint('users', __name__)
api = Namespace('users', description='Users operations')



response_model = api.model('Response', {
    'message': fields.String,
    'status_code': fields.Integer,
    'data': fields.Raw
})

# File upload parser
user_create_parser = api.parser()
user_create_parser.add_argument('first_name', type=str, required=True, help='User first name')
user_create_parser.add_argument('last_name', type=str, required=True, help='User last name')
user_create_parser.add_argument('email', type=str, required=True, help='User email')
user_create_parser.add_argument('password', type=str, required=True, help='User password')
user_create_parser.add_argument('birth_date', type=str, required=True, help='User birth date')
user_create_parser.add_argument('is_active', type=bool, default=True, help='User is active')
user_create_parser.add_argument('user_type_id', type=int, required=True, help='User type ID')
user_create_parser.add_argument('roles', type=str, help='Comma separated role IDs')
user_create_parser.add_argument('picture', type=FileStorage, location='files', help='User picture')

@api.route('/get_all')
class UserList(Resource):
    @api.response(200, 'Success', response_model)
    @jwt_required()
    @api.doc(security='Bearer')
    def get(self):
        """Get all users"""
        return views.get_all(db.session)

@api.route('/get/<int:user_id>')
class UserGet(Resource):
    @api.doc(security='Bearer')  
    @api.response(200, 'Success', response_model)
    @api.response(404, 'User not found')
    @jwt_required()
    def get(self, user_id):
        """Get a user by ID"""
        return views.get_by_id(user_id, db.session)

@api.route('/create')
class UserCreate(Resource):
    @api.expect(user_create_parser)
    @api.response(201, 'User created', response_model)
    def post(self):
        """Create a new user with file upload"""
        args = user_create_parser.parse_args()
        picture_file = args.get('picture')

        # Save picture if exists
        picture_path = None
        if picture_file:
            # Ensure upload directory exists
            upload_dir = os.path.join(os.getcwd(), 'static', 'uploads')
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            
            filename = picture_file.filename
            picture_path = f'static/uploads/{filename}'
            picture_file.save(picture_path)

        # Convert roles string to list if provided
        if args.get('roles'):
            args['roles'] = [int(role_id) for role_id in args['roles'].split(',')]

        # Add picture path to args if exists
        if picture_path:
            args['picture'] = picture_path

        return views.create(schemas.UserCreateSchema(**args), db.session)

@api.route('/update')
class UserUpdate(Resource):
    @api.expect(user_create_parser)
    @api.response(200, 'User updated', response_model)
    @api.response(404, 'User not found')
    @api.doc(security='Bearer')  
    @jwt_required()
    def put(self):
        """Update a user with file upload"""
        current_user_id = get_jwt_identity()  # Get the ID of the current user
        args = user_create_parser.parse_args()
        picture_file = args.get('picture')

        # Save picture if exists
        picture_path = None
        if picture_file:
            upload_dir = os.path.join(os.getcwd(), 'static', 'uploads')
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            
            filename = picture_file.filename
            picture_path = f'static/uploads/{filename}'
            picture_file.save(picture_path)

        # Convert roles string to list if provided
        if args.get('roles'):
            args['roles'] = [int(role_id) for role_id in args['roles'].split(',')]

        # Add picture path to args if exists
        if picture_path:
            args['picture'] = picture_path

        return views.update(schemas.UserUpdateSchema(**args), db.session)

@api.route('/delete/<int:user_id>')
class UserDelete(Resource):
    @api.response(200, 'User deleted')
    @api.response(404, 'User not found')
    @api.doc(security='Bearer')  
    @jwt_required()
    def delete(self, user_id):
        """Delete a user"""
        current_user_id = get_jwt_identity()  # Get the ID of the current user
        return views.delete(user_id, db.session)