"""
Modelo de auditoria
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base

class AuditAction(str, enum.Enum):
    """Ação de auditoria"""
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    EXECUTE = "execute"
    APPROVE = "approve"
    REJECT = "reject"
    LOGIN = "login"
    LOGOUT = "logout"

class AuditLevel(str, enum.Enum):
    """Nível de auditoria"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class AuditLog(Base):
    """Log de auditoria"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Ação
    action = Column(Enum(AuditAction), nullable=False)
    level = Column(Enum(AuditLevel), default=AuditLevel.INFO)
    
    # Descrição
    message = Column(Text, nullable=False)
    details = Column(JSON)
    
    # Contexto
    resource_type = Column(String(50))  # task, infrastructure, user, etc.
    resource_id = Column(Integer)
    
    # Usuário
    user_id = Column(Integer, ForeignKey("users.id"))
    user_ip = Column(String(45))
    user_agent = Column(String(500))
    
    # Metadados
    session_id = Column(String(100))
    request_id = Column(String(100))
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    user = relationship("User")
    
    def __repr__(self):
        return f"<AuditLog(action='{self.action}', level='{self.level}', user_id={self.user_id})>"

class PolicyViolation(Base):
    """Violação de política"""
    __tablename__ = "policy_violations"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Política violada
    policy_name = Column(String(100), nullable=False)
    policy_rule = Column(String(200))
    
    # Detalhes da violação
    violation_message = Column(Text, nullable=False)
    severity = Column(Enum(AuditLevel), default=AuditLevel.WARNING)
    
    # Contexto
    resource_type = Column(String(50))
    resource_id = Column(Integer)
    
    # Ação tomada
    action_taken = Column(String(100))  # blocked, warned, logged
    
    # Usuário
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True))
    
    # Relacionamentos
    user = relationship("User")
    
    def __repr__(self):
        return f"<PolicyViolation(policy='{self.policy_name}', severity='{self.severity}')>"
