"""
Insight Model - Campaign metrics and ROI analytics
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float

from ..core.database import Base


class Insight(Base):
    """Campaign performance metrics and insights"""
    __tablename__ = "insights"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    
    # KPIs
    roi = Column(String(50), nullable=True)  # e.g., "+28%"
    engagement_rate = Column(String(50), nullable=True)  # e.g., "+18%"
    violations_prevented = Column(Integer, default=0)
    
    # Efficiency metrics
    execution_time_seconds = Column(Float, nullable=True)
    agent_success_rate = Column(String(50), nullable=True)  # e.g., "95%"
    
    # Policy compliance
    policies_checked = Column(Integer, default=0)
    policies_passed = Column(Integer, default=0)
    
    # Generated at
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Natural language summary
    summary = Column(String(500), nullable=True)
