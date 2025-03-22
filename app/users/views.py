# views.py
from sqlalchemy.orm import Session
from app.users import models, schemas
from fastapi import HTTPException
from app.user_roles.models import UserRoleDB

def get_all(db: Session):
    try:
        users = db.query(models.UserDB).all()
        user_schemas = [
            schemas.UserResponseSchema.model_validate(user).model_dump(mode="json")
            for user in users
        ]

        response = schemas.BaseResponseSchema(
            message="Users retrieved successfully",
            status_code=200,
            data=user_schemas
        )
        return response.model_dump(mode="json")
    finally:
        db.close()

def get_by_id(user_id: int, db: Session):
    try:
        user = db.query(models.UserDB).filter(models.UserDB.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        response = schemas.BaseResponseSchema(
            message="User retrieved successfully",
            status_code=200,
            data=schemas.UserResponseSchema.model_validate(user).model_dump(mode="json")
        )
        return response.model_dump(mode="json")
    finally:
        db.close()

def create(user: schemas.UserCreateSchema, db: Session):
    try:
        # Create user without roles first
        db_user = models.UserDB(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=user.password,
            birth_date=user.birth_date,
            is_active=user.is_active,
            user_type_id=user.user_type_id
        )
        
        # Add user to session
        db.add(db_user)
        db.flush()  # Flush to get user ID without committing
        
        # Handle roles separately - convert IDs to role objects
        if user.roles:
            role_objects = db.query(UserRoleDB).filter(UserRoleDB.id.in_(user.roles)).all()
            db_user.roles = role_objects
        
        db.commit()
        db.refresh(db_user)
        
        response = schemas.BaseResponseSchema(
            message="User created successfully",
            status_code=201,
            data=schemas.UserResponseSchema.model_validate(db_user).model_dump(mode="json")
        )
        return response.model_dump(mode="json")
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def update(user: schemas.UserUpdateSchema, db: Session):
    try:
        db_user = db.query(models.UserDB).filter(models.UserDB.id == user.id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
       
        # Update basic user fields
        db_user.first_name = user.first_name
        db_user.last_name = user.last_name
        db_user.email = user.email
        db_user.password = user.password
        db_user.birth_date = user.birth_date
        db_user.is_active = user.is_active
        db_user.user_type_id = user.user_type_id
        
        # Handle roles separately - convert IDs to role objects
        if user.roles is not None:
            role_objects = db.query(UserRoleDB).filter(UserRoleDB.id.in_(user.roles)).all()
            db_user.roles = role_objects
        
        db.commit()
        db.refresh(db_user)
        
        response = schemas.BaseResponseSchema(
            message="User updated successfully",
            status_code=200,
            data=schemas.UserResponseSchema.model_validate(db_user).model_dump(mode="json")
        )
        return response.model_dump(mode="json")
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def delete(user: schemas.UserDeleteSchema, db: Session):
    try:
        db_user = db.query(models.UserDB).filter(models.UserDB.id == user.id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        db.delete(db_user)
        db.commit()
        response = schemas.BaseResponseSchema(
            message="User deleted successfully",
            status_code=200,
            data=None
        )
        return response.model_dump(mode="json")
    finally:
        db.close()