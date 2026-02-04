import uuid
from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
from .models import User
from .schemas import UserCreate, UserCreateResponse, LoginRequest, LoginResponse, UserBase
from passlib.context import CryptContext
from src.core.config import settings
from src.core.database import get_db
from datetime import datetime, timedelta
import re
import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def validate_password(password: str) -> bool:
    # Al menos: una mayúscula, una minúscula, un número, un especial (@#$%^&+=), mínimo 8 caracteres
    pattern = (
        r"(?=.*[A-Z])"  # al menos una mayúscula
        r"(?=.*[a-z])"  # al menos una minúscula
        r"(?=.*[0-9])"  # al menos un número
        r"(?=.*[@#$%^&+=])"  # al menos un carácter especial
        r"[A-Za-z0-9@#$%^&+=]{8,}"  # solo caracteres permitidos, mínimo 8
    )
    return re.fullmatch(pattern, password) is not None

def email_exists(db, email: str) -> bool:
    return db.query(User).filter(User.email == email).first() is not None

def create_user(db, user_in: UserCreate) -> UserCreateResponse:
    # 1. Hashear la contraseña
    hashed = pwd_context.hash(user_in.password)

    # 2. Crear instancia del modelo ORM
    db_user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=hashed
    )

    # 3. Persistir
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # 4. Regresar respuesta
    return UserCreateResponse(
        message = "Usuario creado exitosamente",
        id = db_user.id,
        email = db_user.email,
        username = db_user.username
    )

def login_user(db, credentials: LoginRequest) -> LoginResponse:
    # 1. Buscamos usuario mediente su correo electronico
    user_db = db.query(User).filter(User.email == credentials.email).first()

    # 2. Verificamos contraseña
    is_correct = pwd_context.verify(credentials.password, user_db.hashed_password)
    if not is_correct:
        return None

    # 3. Verificamos que el usuairo este activo
    if not user_db.is_active:
        return None

    # 4. Crear token JWT
    data = {"sub": str(user_db.id)}
    access_token = create_access_token(data)

    # Solo exponemos campos seguros
    user_response = UserBase(
        id=user_db.id,
        email=user_db.email,
        username=user_db.username,
        is_active=user_db.is_active,
        created_at=user_db.created_at,
        updated_at=user_db.updated_at,
    )

    return LoginResponse(
        message="Login exitoso",
        access_token=access_token,
        token_type="bearer",
        user=user_response,
    )

def create_access_token(data):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def get_current_user(request: Request, db: Session = Depends(get_db)) -> UserBase:
    # 1. Obtener el token
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado. Inicie sesion para continuar."
        )
    
    # 2. Decodificar y validar el JWT
    token_content = jwt.decode(access_token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    
    # 3. Obtener el identificador del usuario
    user_id = token_content.get("sub", None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El token no contiene el ID del usuario autenticado"
        )
    
    # 4. Obtener usuario desde la BD (sub viene como string, User.id es UUID)
    user_db = db.query(User).filter(User.id == uuid.UUID(user_id)).first()
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontro el usuario en la base de datos"
        )
    
    # 5. Devolver usuario
    return UserBase(
        id=user_db.id,
        email=user_db.email,
        username=user_db.username,
        is_active=user_db.is_active,
        created_at=user_db.created_at,
        updated_at=user_db.updated_at,
    )