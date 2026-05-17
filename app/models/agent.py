"""
Agent Model - Tracks execution status of orchestrated agents
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from enum import Enum

from ..core.database import Base


class AgentStatus(str, Enum):
    """Agent execution states"""
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"
    warning = "warning"


class Agent(Base):
    """Represents an individual agent in the orchestration"""
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    
    name = Column(String(255), index=True)
    role = Column(String(100))  # e.g., "Trend Analyzer", "Brand Safety"
    status = Column(SQLEnum(AgentStatus), default=AgentStatus.pending)
    
    # Execution details
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Result summary
    result_summary = Column(String(500), nullable=True)
    error_message = Column(String(500), nullable=True)
