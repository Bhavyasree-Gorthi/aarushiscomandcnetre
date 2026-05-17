"""
Campaign Model - Orchestration tracking for multi-agent workflows
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum
from enum import Enum

from ..core.database import Base


class CampaignStatus(str, Enum):
    """Campaign execution states"""
    draft = "draft"
    running = "running"
    completed = "completed"
    failed = "failed"
    paused = "paused"


class Campaign(Base):
    """Represents a campaign orchestration workflow"""
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(Text, nullable=True)
    status = Column(SQLEnum(CampaignStatus), default=CampaignStatus.draft)
    
    # Supervity orchestration ID
    orchestration_id = Column(String(255), nullable=True, unique=True)
    
    # Timeline and execution tracking
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Business metrics
    roi = Column(String(50), nullable=True)  # e.g., "+28%"
    engagement = Column(String(50), nullable=True)  # e.g., "+18%"
    violations_prevented = Column(Integer, default=0)
