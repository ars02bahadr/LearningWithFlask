from typing import Optional, Any
from pydantic import BaseModel
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
    pass

class UserTypeUpdateSchema(UserTypeBaseSchema):
    pass
class UserTypeDeleteSchema(BaseModel):
    id: int