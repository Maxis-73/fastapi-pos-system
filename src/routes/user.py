from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.schemas.user import UserCreate, UserCreateResponse
from src.services.user import create_user, email_exists, validate_password

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/create", response_model=UserCreateResponse)
async def register(user_in: UserCreate, db: Session = Depends(get_db)):
    # 1. Verificar que el correo no exista
    result = email_exists(db, user_in.email)
    if result:
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")

    # 2. Verificar contraseña
    valid_password = validate_password(user_in.password)
    if not valid_password:
        raise HTTPException(
            status_code=400, 
            detail="La contraseña debe tener al menos 8 caracteres y contener al menos una letra mayúscula, una letra minúscula, un número y un carácter especial"
        )

    # 3. Crear usuario
    return create_user(db, user_in)