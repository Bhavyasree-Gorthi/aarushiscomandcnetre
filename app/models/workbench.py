"""
Workbench Model - Human-in-the-loop review queue
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from enum import Enum

from ..core.database import Base


class WorkbenchStatus(str, Enum):
    """Review item states"""
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    escalated = "escalated"


class WorkbenchItem(Base):
    """Represents an item requiring human review in the workbench"""
    __tablename__ = "workbench_items"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    
    title = Column(String(255), index=True)
    description = Column(Text)
    issue_type = Column(String(100))  # e.g., "policy_violation", "uncertain_decision"
    
    # Status and action tracking
    status = Column(SQLEnum(WorkbenchStatus), default=WorkbenchStatus.pending)
    
    # Who should review this
    assigned_to = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)
    review_notes = Column(Text, nullable=True)
    
    # Context for decision
    related_policy = Column(String(255), nullable=True)
    suggested_action = Column(String(500), nullable=True)
