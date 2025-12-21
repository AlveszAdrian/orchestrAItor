"""
API v1 routes
"""

from fastapi import APIRouter
from .endpoints import auth, tasks, infrastructure, chat, audit

api_router = APIRouter()

# Incluir todas as rotas
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(infrastructure.router, prefix="/infrastructure", tags=["infrastructure"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(audit.router, prefix="/audit", tags=["audit"])
