from src.models.user import User
from src.schemas.user import UserCreate, UserCreateResponse
from passlib.context import CryptContext
import re

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