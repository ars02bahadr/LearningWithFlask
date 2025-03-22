from typing import Optional, Any
from pydantic import BaseModel
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
    pass

class UserRoleUpdateSchema(UserRoleBaseSchema):
    pass
class UserRoleDeleteSchema(BaseModel):
    id: int