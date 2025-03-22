# views.py
from sqlalchemy.orm import Session
from app.user_roles import models, schemas
from fastapi import HTTPException

def get_all(db: Session):
    try:
        user_roles = db.query(models.UserRoleDB).all()
        user_role_schemas = [
            schemas.UserRoleResponseSchema.model_validate(user_role).model_dump(mode="json")
            for user_role in user_roles
        ]

        response = schemas.BaseResponseSchema(
            message="User roles retrieved successfully",
            status_code=200,
            data=user_role_schemas
        )
        return response.model_dump(mode="json")
    finally:
        db.close()

def get_by_id(user_role_id: int, db: Session):
    try:
        user_role = db.query(models.UserRoleDB).filter(models.UserRoleDB.id == user_role_id).first()
        if user_role is None:
            raise HTTPException(status_code=404, detail="User role not found")
        response = schemas.BaseResponseSchema(
            message="User role retrieved successfully",
            status_code=200,
            data=schemas.UserRoleResponseSchema.model_validate(user_role).model_dump(mode="json")
        )
        return response.model_dump(mode="json")
    finally:
        db.close()

def create(user_role: schemas.UserRoleCreateSchema, db: Session):
    try:
        db_user_role = models.UserRoleDB(name=user_role.name)
        db.add(db_user_role)
        db.commit()
        db.refresh(db_user_role)

        response = schemas.BaseResponseSchema(
            message="User role created successfully",
            status_code=201,
            data=schemas.UserRoleResponseSchema.model_validate(db_user_role).model_dump(mode="json")
        )
        return response.model_dump(mode="json")
    finally:
        db.close()


def update(user_role: schemas.UserRoleUpdateSchema, db: Session):
    try:
        db_user_role = db.query(models.UserRoleDB).filter(models.UserRoleDB.id == user_role.id).first()
        if db_user_role is None:
            raise HTTPException(status_code=404, detail="User role not found")
        
        db_user_role.name = user_role.name
        db.commit()
        db.refresh(db_user_role)
        response = schemas.BaseResponseSchema(
            message="User role updated successfully",
            status_code=200,
            data=schemas.UserRoleResponseSchema.model_validate(db_user_role).model_dump(mode="json")
        )
        return response.model_dump(mode="json")
    finally:
        db.close()

def delete(user_role: schemas.UserRoleDeleteSchema, db: Session):
    try:
        db_user_role = db.query(models.UserRoleDB).filter(models.UserRoleDB.id == user_role.id).first()
        if db_user_role is None:
            raise HTTPException(status_code=404, detail="User role not found")
        
        db.delete(db_user_role)
        db.commit()
        response = schemas.BaseResponseSchema(
            message="User role deleted successfully",
            status_code=200,
            data=None
        )
        return response.model_dump(mode="json")
    finally:
        db.close()