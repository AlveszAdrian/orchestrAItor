"""
Agente Autônomo de Infraestrutura com Governança
Backend API Principal
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import structlog
import uvicorn

from app.core.config import settings
from app.core.database import init_db
from app.api.v1 import api_router
from app.core.logging import setup_logging

# Configurar logging estruturado
setup_logging()
logger = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerenciar ciclo de vida da aplicação"""
    logger.info("Iniciando Agente de Infraestrutura...")
    
    # Inicializar banco de dados
    await init_db()
    logger.info("Banco de dados inicializado")
    
    yield
    
    logger.info("Finalizando aplicação...")

# Criar instância FastAPI
app = FastAPI(
    title="Agente Autônomo de Infraestrutura",
    description="Sistema de IA para automação segura de infraestrutura",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas da API
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "Agente Autônomo de Infraestrutura",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "orchestrator-backend"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
