from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import db
from app.users.models import user_roles

class UserRoleDB(db.Model):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    # Many-to-Many relationship with User (bir rolün birden fazla user'ı olabilir)
    users = relationship('UserDB', secondary=user_roles, back_populates='roles')
