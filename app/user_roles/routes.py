# routes.py
from flask import Blueprint, request
from flask_restx import Api, Resource, Namespace, fields
from app.database import db
from app.user_roles import views, schemas
from pydantic import ValidationError

user_roles_bp = Blueprint('user_roles', __name__)
api = Namespace('user-roles', description='User Roles operations')

user_role_create_model = api.model(
    'UserRoleCreate',
    {'name': fields.String(required=True, description='User Role name')})

user_role_update_model = api.model(
    'UserRoleUpdate', {
        'id': fields.Integer(required=True, description='User Role ID'),
        'name': fields.String(required=True, description='User Role name')
    })

user_role_delete_model = api.model(
    'UserRoleDelete',
    {'id': fields.Integer(required=True, description='User Role ID')})

response_model = api.model(
    'ResponseModel', {
        'message': fields.String(required=True),
        'status_code': fields.Integer(required=True),
        'data': fields.Raw()
    })


@api.route('/get_all')
class UserRoleList(Resource):

    @api.response(200, 'Success', response_model)
    def get(self):
        """Get all user roles"""
        return views.get_all(db.session)


@api.route('/get_by_id')
class UserRoleById(Resource):

    @api.response(200, 'Success', response_model)
    @api.response(404, 'User Role not found')
    @api.doc(params={'id': 'User Role ID'})
    def get(self):
        """Get a user role by ID"""
        user_role_id = request.args.get('id', type=int)
        return views.get_by_id(user_role_id, db.session)


@api.route('/create')
class UserRoleCreate(Resource):

    @api.response(201, 'User Role created', response_model)
    @api.expect(user_role_create_model)
    def post(self):
        """Create a new user role"""
        data = request.get_json()

        try:
            validated = schemas.UserRoleCreateSchema(**data)
        except ValidationError as ve:
            errors = ve.errors()
            return {
                "message": errors[0]['msg'] if errors else "Validation error",
                "status_code": 400,
                "data": None
            }, 400

        return views.create(validated, db.session)


@api.route('/update')
class UserRoleUpdate(Resource):

    @api.response(200, 'User Role updated', response_model)
    @api.response(404, 'User Role not found')
    @api.expect(user_role_update_model)
    def put(self):
        """Update a user role"""
        data = request.get_json()

        try:
            validated = schemas.UserRoleUpdateSchema(**data)
        except ValidationError as ve:
            errors = ve.errors()
            return {
                "message": errors[0]['msg'] if errors else "Validation error",
                "status_code": 400,
                "data": None
            }, 400

        return views.update(validated, db.session)


@api.route('/delete')
class UserRoleDelete(Resource):

    @api.response(200, 'User Role deleted', response_model)
    @api.response(404, 'User Role not found')
    @api.expect(user_role_delete_model)
    def delete(self):
        """Delete a user role"""
        data = request.get_json()
        return views.delete(schemas.UserRoleDeleteSchema(**data), db.session)
