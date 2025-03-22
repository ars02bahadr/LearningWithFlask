# routes.py
from flask import Blueprint, request
from flask_restx import Api, Resource, Namespace, fields
from app.database import db
from app.user_types import views, schemas

user_types_bp = Blueprint('user_types', __name__)
api = Namespace('user-types', description='User Types operations')

# Define Flask-RESTX models based on your Pydantic schemas

user_type_create_model = api.model('UserTypeCreate', {
    'name': fields.String(required=True, description='User Type name')
})

user_type_update_model = api.model('UserTypeUpdate', {
    'id': fields.Integer(required=True, description='User Type ID'),
    'name': fields.String(required=True, description='User Type name')
})

user_type_delete_model = api.model('UserTypeDelete', {
    'id': fields.Integer(required=True, description='User Type ID')
})

response_model = api.model('ResponseModel', {
    'message': fields.String(required=True),
    'status_code': fields.Integer(required=True),
    'data': fields.Raw()
})

@api.route('/get_all')
class UserTypeList(Resource):
    @api.response(200, 'Success', response_model)
    def get(self):
        """Get all user types"""
        return views.get_all(db.session)

@api.route('/get_by_id')
class UserTypeById(Resource):
    @api.response(200, 'Success', response_model)
    @api.response(404, 'User Type not found')
    @api.doc(params={'id': 'User Type ID'})
    def get(self):
        """Get a user type by ID"""
        user_type_id = request.args.get('id', type=int)
        return views.get_by_id(user_type_id, db.session)

@api.route('/create')
class UserTypeCreate(Resource):
    @api.response(201, 'User Type created', response_model)
    @api.expect(user_type_create_model)
    def post(self):
        """Create a new user type"""
        data = request.get_json()
        return views.create(schemas.UserTypeCreateSchema(**data), db.session)

@api.route('/update')
class UserTypeUpdate(Resource):
    @api.response(200, 'User Type updated', response_model)
    @api.response(404, 'User Type not found')
    @api.expect(user_type_update_model)
    def put(self):
        """Update a user type"""
        data = request.get_json()
        return views.update(schemas.UserTypeUpdateSchema(**data), db.session)

@api.route('/delete')
class UserTypeDelete(Resource):
    @api.response(200, 'User Type deleted', response_model)
    @api.response(404, 'User Type not found')
    @api.expect(user_type_delete_model)
    def delete(self):
        """Delete a user type"""
        data = request.get_json()
        return views.delete(schemas.UserTypeDeleteSchema(**data), db.session)