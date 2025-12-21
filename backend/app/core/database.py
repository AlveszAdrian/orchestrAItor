"""
Configuração do banco de dados
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import structlog

from .config import settings

logger = structlog.get_logger()

# Engine assíncrono
engine = create_async_engine(
    settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    echo=settings.DEBUG,
    future=True
)

# Session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    """Base class para modelos SQLAlchemy"""
    pass

async def get_db() -> AsyncSession:
    """Dependency para obter sessão do banco"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    """Inicializar banco de dados"""
    try:
        async with engine.begin() as conn:
            # Importar todos os modelos aqui para criar as tabelas
            from app.models import user, task, infrastructure, audit
            
            # Criar todas as tabelas
            await conn.run_sync(Base.metadata.create_all)
            
        logger.info("Banco de dados inicializado com sucesso")
    except Exception as e:
        logger.error("Erro ao inicializar banco de dados", error=str(e))
        raise
