"""
Workbench Schemas - Request/response models for human review queue
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class WorkbenchItemBase(BaseModel):
    title: str
    description: str
    issue_type: str


class WorkbenchItemCreate(WorkbenchItemBase):
    campaign_id: int
    assigned_to: Optional[str] = None
    related_policy: Optional[str] = None
    suggested_action: Optional[str] = None


class WorkbenchItem(WorkbenchItemBase):
    id: int
    campaign_id: int
    status: str
    assigned_to: Optional[str] = None
    created_at: datetime
    reviewed_at: Optional[datetime] = None
    review_notes: Optional[str] = None
    related_policy: Optional[str] = None
    suggested_action: Optional[str] = None

    class Config:
        orm_mode = True


class WorkbenchApprovalRequest(BaseModel):
    """Request to approve/reject a workbench item"""
    review_id: int
    status: str  # "approved", "rejected"
    notes: Optional[str] = None


class WorkbenchQueueResponse(BaseModel):
    """Workbench queue status"""
    total_items: int
    pending: int
    approved: int
    rejected: int
    items: list[WorkbenchItem] = []
