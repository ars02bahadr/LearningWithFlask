from app.users.models import UserDB
from app.auth import schemas
from sqlalchemy.orm import Session
from flask_jwt_extended import create_access_token
from datetime import timedelta

def login(login_data: schemas.LoginRequest, db: Session):
    """
    Login user and return JWT token
    """
    # Find user by email
    user = db.query(UserDB).filter(UserDB.email == login_data.email).first()
    
    if not user:
        return schemas.BaseResponseSchema(
            message="Invalid email or password",
            status_code=401,
            data=None
        ).model_dump()

    # Check password (plain text comparison for now)
    if user.password != login_data.password:
        return schemas.BaseResponseSchema(
            message="Invalid email or password",
            status_code=401,
            data=None
        ).model_dump()

    # Create access token
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            'email': user.email,
            'roles': [role.id for role in user.roles],
            'user_type': user.user_type_id
        },
    expires_delta=timedelta(days=1)
)

    return schemas.BaseResponseSchema(
        message="Login successful",
        status_code=200,
        data={
            'access_token': access_token,
            'token_type': 'bearer'
        }
    ).model_dump()

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )