"""
Policy Schemas - Request/response models for governance policies
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PolicyBase(BaseModel):
    name: str
    description: Optional[str] = None
    rule_text: str


class PolicyCreate(PolicyBase):
    campaign_id: Optional[int] = None
    source_document: Optional[str] = None


class Policy(PolicyBase):
    id: int
    campaign_id: Optional[int] = None
    status: str
    is_active: bool
    triggered_at: Optional[datetime] = None
    created_at: datetime
    source_document: Optional[str] = None

    class Config:
        orm_mode = True


class PolicyEvent(BaseModel):
    """Policy enforcement event"""
    policy: str
    status: str
    campaign: str
    triggered_at: datetime
    severity: str = "warning"  # "info", "warning", "critical"
