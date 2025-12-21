"""
Endpoints de autenticação
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import timedelta
import structlog

from app.core.security import (
    verify_password, 
    get_password_hash, 
    create_access_token,
    get_current_user
)
from app.core.config import settings

logger = structlog.get_logger()
router = APIRouter()

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    role: str
    is_active: bool

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    """Registrar novo usuário"""
    try:
        # Implementar registro de usuário
        # Por enquanto, retorna exemplo
        return UserResponse(
            id=1,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            role="viewer",
            is_active=True
        )
    except Exception as e:
        logger.error("Erro no registro", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro no registro"
        )

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login do usuário"""
    try:
        # Implementar verificação de usuário
        # Por enquanto, aceita qualquer usuário
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": form_data.username, "username": form_data.username},
            expires_delta=access_token_expires
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
        
    except Exception as e:
        logger.error("Erro no login", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Obter informações do usuário atual"""
    return UserResponse(
        id=1,
        username=current_user["username"],
        email="user@example.com",
        full_name="Usuario Exemplo",
        role="admin",
        is_active=True
    )
