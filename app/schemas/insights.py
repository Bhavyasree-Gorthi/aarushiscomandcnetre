"""
Insights Schemas - Request/response models for analytics
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class InsightBase(BaseModel):
    roi: Optional[str] = None
    engagement_rate: Optional[str] = None
    violations_prevented: int = 0


class Insight(InsightBase):
    id: int
    campaign_id: int
    execution_time_seconds: Optional[float] = None
    agent_success_rate: Optional[str] = None
    policies_checked: int
    policies_passed: int
    created_at: datetime
    summary: Optional[str] = None

    class Config:
        orm_mode = True


class InsightsResponse(BaseModel):
    """Campaign insights summary"""
    roi: str
    engagement: str
    violations_prevented: int
    execution_time: Optional[str] = None
    agent_success_rate: Optional[str] = None
    policies_compliance: Optional[str] = None
    summary: Optional[str] = None
