from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from src.core.database import get_db
from .schemas import UserCreate, UserCreateResponse, LoginRequest, LoginResponse
from .service import create_user, email_exists, validate_password, login_user
from src.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/create", response_model=UserCreateResponse)
async def register(user_in: UserCreate, db: Session = Depends(get_db)):
    # 1. Verificar que el correo no exista
    result = email_exists(db, user_in.email)
    if result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El correo electrónico ya está registrado"
        )

    # 2. Verificar contraseña
    valid_password = validate_password(user_in.password)
    if not valid_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="La contraseña debe tener al menos 8 caracteres y contener al menos una letra mayúscula, una letra minúscula, un número y un carácter especial"
        )

    # 3. Crear usuario
    return create_user(db, user_in)

@router.post("/login", response_model=LoginResponse)
async def login(credentials: LoginRequest, response: Response, db: Session = Depends(get_db)):
    # 1. Verificamos que el email exista
    exists = email_exists(db, credentials.email)
    if not exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico no esta registrado"
        )

    # 2. Loggear usuario
    result = login_user(db, credentials)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No es posible iniciar sesión. Verifique sus credenciales o el estado del usuario"
        )

    # 3. Establecemos la cookie correspondiente
    response.set_cookie(
        key="access_token",
        value=result.access_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=settings.ACCESS_TOKEN_EXPIRE_HOURS * 3600,
    )

    return result