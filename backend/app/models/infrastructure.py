"""
Modelo de infraestrutura
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, JSON, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base

class InfrastructureType(str, enum.Enum):
    """Tipo de infraestrutura"""
    SERVER = "server"
    CONTAINER = "container"
    DATABASE = "database"
    NETWORK = "network"
    STORAGE = "storage"
    SECURITY = "security"
    MONITORING = "monitoring"

class InfrastructureStatus(str, enum.Enum):
    """Status da infraestrutura"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PROVISIONING = "provisioning"
    DECOMMISSIONING = "decommissioning"
    ERROR = "error"
    MAINTENANCE = "maintenance"

class CloudProvider(str, enum.Enum):
    """Provedor de nuvem"""
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    ON_PREMISE = "on_premise"
    HYBRID = "hybrid"

class Infrastructure(Base):
    """Modelo de infraestrutura"""
    __tablename__ = "infrastructure"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    
    # Tipo e provider
    type = Column(Enum(InfrastructureType), nullable=False)
    provider = Column(Enum(CloudProvider), nullable=False)
    
    # Status
    status = Column(Enum(InfrastructureStatus), default=InfrastructureStatus.ACTIVE)
    
    # Configuração
    configuration = Column(JSON)  # Configuração atual
    desired_configuration = Column(JSON)  # Configuração desejada
    
    # Localização
    region = Column(String(50))
    availability_zone = Column(String(50))
    
    # Recursos
    cpu_cores = Column(Integer)
    memory_gb = Column(Integer)
    storage_gb = Column(Integer)
    
    # Rede
    ip_address = Column(String(45))  # IPv4 ou IPv6
    hostname = Column(String(100))
    
    # Metadados
    tags = Column(JSON)
    cost_per_hour = Column(String(20))  # Decimal como string
    
    # Relacionamentos
    managed_by = Column(Integer, ForeignKey("users.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_health_check = Column(DateTime(timezone=True))
    
    # Relacionamentos
    manager = relationship("User")
    
    def __repr__(self):
        return f"<Infrastructure(name='{self.name}', type='{self.type}', status='{self.status}')>"

class InfrastructureTemplate(Base):
    """Template de infraestrutura"""
    __tablename__ = "infrastructure_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    
    # Tipo de template
    type = Column(Enum(InfrastructureType), nullable=False)
    
    # Template files
    terraform_template = Column(Text)
    ansible_playbook = Column(Text)
    helm_chart = Column(Text)
    
    # Configuração padrão
    default_configuration = Column(JSON)
    
    # Metadados
    version = Column(String(20))
    is_active = Column(Boolean, default=True)
    
    # Relacionamentos
    created_by = Column(Integer, ForeignKey("users.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    creator = relationship("User")
    
    def __repr__(self):
        return f"<InfrastructureTemplate(name='{self.name}', version='{self.version}')>"
