from app.database import db
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship

# Association table for User-Role many-to-many relationship
user_roles = Table(
    'user_roles_association',
    db.Model.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('user_roles.id'))
)

class UserDB(db.Model):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), index=True)
    last_name = Column(String(100), index=True)
    email = Column(String(100), index=True, unique=True)
    password = Column(String(100))
    birth_date = Column(Date, index=True)
    is_active = Column(Boolean, default=True)
    picture = Column(String(700))
    
    # One-to-Many relationship with UserType (bir kullanıcının bir tipi olur)
    user_type_id = Column(Integer, ForeignKey('user_types.id'))
    user_type = relationship('UserTypeDB', back_populates='users')
    
    # Many-to-Many relationship with UserRole (bir kullanıcının birden fazla rolü olabilir)
    roles = relationship('UserRoleDB', secondary=user_roles, back_populates='users')
