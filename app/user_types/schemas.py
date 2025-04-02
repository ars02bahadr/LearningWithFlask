from typing import Optional, Any
from pydantic import BaseModel, Field, field_validator
import datetime


class BaseSchema(BaseModel):
    id: Optional[int] = None


class BaseResponseSchema(BaseModel):
    message: str
    status_code: int
    data: Optional[Any] = None


class UserTypeBaseSchema(BaseSchema):
    name: str

    class Config:
        from_attributes = True


class UserTypeResponseSchema(BaseModel):
    id: int
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True


class UserTypeCreateSchema(UserTypeBaseSchema):

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if len(v.strip()) == 0:
            raise ValueError("Kullanıcı tipi adı boş olamaz")
        if len(v) > 50:
            raise ValueError("Kullanıcı tipi adı 50 karakterden uzun olamaz")
        return v


class UserTypeUpdateSchema(UserTypeBaseSchema):
    pass


class UserTypeDeleteSchema(BaseModel):
    id: int
