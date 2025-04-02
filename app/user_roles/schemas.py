from typing import Optional, Any
from pydantic import BaseModel, Field, field_validator
import datetime


class BaseSchema(BaseModel):
    id: Optional[int] = None


class BaseResponseSchema(BaseModel):
    message: str
    status_code: int
    data: Optional[Any] = None


class UserRoleBaseSchema(BaseSchema):
    name: str

    class Config:
        from_attributes = True


class UserRoleResponseSchema(BaseModel):
    id: int
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True


class UserRoleCreateSchema(UserRoleBaseSchema):

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if len(v.strip()) == 0:
            raise ValueError(
                "Lütfen geçerli bir kullanıcı tipi adı giriniz. Boş bir değer kabul edilemez."
            )
        if len(v) > 50:
            raise ValueError(
                "Kullanıcı tipi adı çok uzun. Lütfen 50 karakterden kısa bir isim giriniz."
            )
        return v


class UserRoleUpdateSchema(UserRoleBaseSchema):

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if len(v.strip()) == 0:
            raise ValueError(
                "Lütfen geçerli bir kullanıcı tipi adı giriniz. Boş bir değer kabul edilemez."
            )
        if len(v) > 50:
            raise ValueError(
                "Kullanıcı tipi adı çok uzun. Lütfen 50 karakterden kısa bir isim giriniz."
            )
        return v


class UserRoleDeleteSchema(BaseModel):
    id: int
