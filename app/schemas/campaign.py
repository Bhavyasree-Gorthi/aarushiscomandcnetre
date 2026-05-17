"""
Campaign Schemas - Request/response models for campaign management
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CampaignBase(BaseModel):
    name: str
    description: Optional[str] = None


class CampaignCreate(CampaignBase):
    pass


class CampaignUpdate(BaseModel):
    status: Optional[str] = None
    roi: Optional[str] = None
    engagement: Optional[str] = None
    violations_prevented: Optional[int] = None


class Campaign(CampaignBase):
    id: int
    status: str
    orchestration_id: Optional[str] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    roi: Optional[str] = None
    engagement: Optional[str] = None
    violations_prevented: int

    class Config:
        orm_mode = True


class CampaignRunRequest(BaseModel):
    """Request to launch a campaign via Supervity"""
    campaign: str  # Campaign name
    context: Optional[dict] = None


class CampaignStatusResponse(BaseModel):
    """Campaign execution status with agent timeline"""
    campaign: Campaign
    agents: list = []
    timeline: list = []
    policy_violations: int = 0
