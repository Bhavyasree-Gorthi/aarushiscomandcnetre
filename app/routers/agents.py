"""
Agents Router - Agent execution tracking and status updates

This router handles:
- Agent status updates from Supervity
- Agent execution history
- Agent performance metrics
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.models import Agent, Campaign
from app.schemas import Agent as AgentSchema, AgentCreate, AgentStatusUpdate
from app.security import get_current_user

log = logging.getLogger(__name__)

router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("/{campaign_id}/report", status_code=status.HTTP_200_OK)
async def report_agent_status(
    campaign_id: int,
    agent_name: str,
    update: AgentStatusUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """
    Report agent execution status (called by Supervity webhooks).
    
    This endpoint receives agent status updates and stores them for visibility.
    """
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    # Find or create agent
    agent = db.query(Agent).filter(
        Agent.campaign_id == campaign_id,
        Agent.name == agent_name,
    ).first()
    
    if not agent:
        agent = Agent(
            campaign_id=campaign_id,
            name=agent_name,
            role=agent_name,  # Can be updated
            status=update.status,
        )
        db.add(agent)
    else:
        agent.status = update.status
    
    if update.result_summary:
        agent.result_summary = update.result_summary
    if update.error_message:
        agent.error_message = update.error_message
    
    if update.status == "completed":
        agent.completed_at = datetime.utcnow()
    elif update.status == "running":
        agent.started_at = datetime.utcnow()
    
    db.commit()
    db.refresh(agent)
    
    log.info(f"[AGENT] {agent_name} status: {update.status}")
    
    return {
        "agent_id": agent.id,
        "status": agent.status,
        "message": f"Agent '{agent_name}' status updated",
    }


@router.get("/{campaign_id}", response_model=list)
async def list_campaign_agents(
    campaign_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Get all agents for a campaign."""
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    agents = db.query(Agent).filter(Agent.campaign_id == campaign_id).all()
    return agents


@router.get("/{agent_id}/history", response_model=dict)
async def get_agent_history(
    agent_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Get execution history for an agent."""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return {
        "agent_id": agent.id,
        "name": agent.name,
        "role": agent.role,
        "status": agent.status,
        "started_at": agent.started_at,
        "completed_at": agent.completed_at,
        "duration": (
            (agent.completed_at - agent.started_at).total_seconds()
            if agent.completed_at and agent.started_at
            else None
        ),
        "result": agent.result_summary,
        "error": agent.error_message,
    }
