"""
Endpoints de auditoria
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
import structlog

from app.core.security import get_current_user, require_admin

logger = structlog.get_logger()
router = APIRouter()

class AuditLogResponse(BaseModel):
    id: int
    action: str
    message: str
    user_id: int
    created_at: str

@router.get("/logs", response_model=List[AuditLogResponse])
async def get_audit_logs(current_user: dict = Depends(require_admin)):
    """Obter logs de auditoria"""
    return []
