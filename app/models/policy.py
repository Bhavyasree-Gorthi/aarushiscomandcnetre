"""
Policy Model - Business rules and governance constraints
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum, Boolean
from enum import Enum

from ..core.database import Base


class PolicyStatus(str, Enum):
    """Policy enforcement outcomes"""
    passed = "passed"
    failed = "failed"
    warning = "warning"


class Policy(Base):
    """Represents a governance policy for campaign execution"""
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True)
    
    name = Column(String(255), index=True)
    description = Column(Text, nullable=True)
    
    # Policy definition (can reference RAG-indexed documents)
    rule_text = Column(Text)  # e.g., "No health claims without FDA approval"
    
    # Enforcement status
    status = Column(SQLEnum(PolicyStatus), default=PolicyStatus.passed)
    is_active = Column(Boolean, default=True)
    
    # When this policy was triggered
    triggered_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Reference to related document
    source_document = Column(String(255), nullable=True)  # e.g., "brand_guidelines.pdf"
