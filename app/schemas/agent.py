"""
Agent Schemas - Request/response models for agent tracking
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AgentBase(BaseModel):
    name: str
    role: str


class AgentCreate(AgentBase):
    campaign_id: int
    status: str = "pending"


class Agent(AgentBase):
    id: int
    campaign_id: int
    status: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result_summary: Optional[str] = None
    error_message: Optional[str] = None

    class Config:
        orm_mode = True


class AgentStatusUpdate(BaseModel):
    status: str
    result_summary: Optional[str] = None
    error_message: Optional[str] = None
