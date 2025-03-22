# views.py
from sqlalchemy.orm import Session
from app.user_types import models, schemas
from fastapi import HTTPException

def get_all(db: Session):
    try:
        user_types = db.query(models.UserTypeDB).all()
        user_type_schemas = [
            schemas.UserTypeResponseSchema.model_validate(user_type).model_dump(mode="json")
            for user_type in user_types
        ]

        response = schemas.BaseResponseSchema(
            message="User types retrieved successfully",
            status_code=200,
            data=user_type_schemas
        )
        return response.model_dump(mode="json")
    finally:
        db.close()

def get_by_id(user_type_id: int, db: Session):
    try:
        user_type = db.query(models.UserTypeDB).filter(models.UserTypeDB.id == user_type_id).first()
        if user_type is None:
            raise HTTPException(status_code=404, detail="User type not found")
        response = schemas.BaseResponseSchema(
            message="User type retrieved successfully",
            status_code=200,
            data=schemas.UserTypeResponseSchema.model_validate(user_type).model_dump(mode="json")
        )
        return response.model_dump(mode="json")
    finally:
        db.close()

def create(user_type: schemas.UserTypeCreateSchema, db: Session):
    try:
        db_user_type = models.UserTypeDB(name=user_type.name)
        db.add(db_user_type)
        db.commit()
        db.refresh(db_user_type)

        response = schemas.BaseResponseSchema(
            message="User type created successfully",
            status_code=201,
            data=schemas.UserTypeResponseSchema.model_validate(db_user_type).model_dump(mode="json")
        )
        return response.model_dump(mode="json")
    finally:
        db.close()


def update(user_type: schemas.UserTypeUpdateSchema, db: Session):
    try:
        db_user_type = db.query(models.UserTypeDB).filter(models.UserTypeDB.id == user_type.id).first()
        if db_user_type is None:
            raise HTTPException(status_code=404, detail="User type not found")
        
        db_user_type.name = user_type.name
        db.commit()
        db.refresh(db_user_type)
        response = schemas.BaseResponseSchema(
            message="User type updated successfully",
            status_code=200,
            data=schemas.UserTypeResponseSchema.model_validate(db_user_type).model_dump(mode="json")
        )
        return response.model_dump(mode="json")
    finally:
        db.close()

def delete(user_type: schemas.UserTypeDeleteSchema, db: Session):
    try:
        db_user_type = db.query(models.UserTypeDB).filter(models.UserTypeDB.id == user_type.id).first()
        if db_user_type is None:
            raise HTTPException(status_code=404, detail="User type not found")
        
        db.delete(db_user_type)
        db.commit()
        response = schemas.BaseResponseSchema(
            message="User type deleted successfully",
            status_code=200,
            data=None
        )
        return response.model_dump(mode="json")
    finally:
        db.close()