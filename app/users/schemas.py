from typing import Optional, Any, List
from pydantic import BaseModel
import datetime

from app.user_types.schemas import UserTypeResponseSchema
from app.user_roles.schemas import UserRoleResponseSchema


class BaseSchema(BaseModel):
    id: Optional[int] = None

class BaseResponseSchema(BaseModel):
    message: str
    status_code: int
    data: Optional[Any] = None

class UserBaseSchema(BaseSchema):
    first_name: str
    last_name: str
    email: str
    password: str
    birth_date: datetime.date
    is_active: bool
    user_type_id: int
    roles: Optional[List[int]] = None
    picture: Optional[str] = None

    class Config:
        from_attributes = True

class UserResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    birth_date: datetime.date
    is_active: bool
    user_type_id: int
    user_type: Optional[UserTypeResponseSchema] = None
    roles: Optional[List[UserRoleResponseSchema]] = None
    
    class Config:
        from_attributes = True  

class UserCreateSchema(UserBaseSchema):
    pass

class UserUpdateSchema(UserBaseSchema):
    pass
class UserDeleteSchema(BaseModel):
    id: int