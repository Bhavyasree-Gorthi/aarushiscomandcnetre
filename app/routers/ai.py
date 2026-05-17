from datetime import datetime
from typing import Any, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.routers.campaign import campaign_status, run_campaign
from app.routers.insights import insights
from app.routers.policies import policy_events
from app.routers.workbench import workbench_reviews

from app.models.policy import Policy as PolicyModel
from app.models.policy import PolicyStatus


router = APIRouter(prefix="/ai", tags=["AI"])


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[ChatMessage] = Field(default_factory=list)
    context: Optional[dict] = None


class ToolCall(BaseModel):
    id: str
    name: str
    args: dict
    result: Optional[Any] = None


class ChatResponse(BaseModel):
    response: str
    tool_calls: Optional[list[ToolCall]] = None


class PolicyInputRequest(BaseModel):
    input: str


class PolicyConflictRequest(BaseModel):
    natural_language: str
    policy_scope: str = "base"
    entity_name: Optional[str] = None


class PolicyTranslateRequest(BaseModel):
    natural_language: str


class PolicyAnalyzeRequest(BaseModel):
    natural_language: str
    policy_type: Optional[str] = None
    entity_name: Optional[str] = None


class PolicyPayload(BaseModel):
    name: str
    description: str = ""
    natural_language: str
    policy_type: str = "logical"
    dsl: Optional[dict] = None
    refined_instruction: Optional[str] = None
    entity_name: Optional[str] = None
    priority: int = 50
    tags: list[str] = Field(default_factory=list)
    is_active: bool = True


def extract_campaign_topic(message: str) -> str:
    lower_message = message.lower()
    for marker in (" for ", " about ", " on "):
        if marker in lower_message:
            start = lower_message.rfind(marker) + len(marker)
            topic = message[start:].strip(" .")
            if topic:
                return topic

    return "AI in Healthcare"


def looks_like_campaign_topic(message: str) -> bool:
    words = message.strip().split()
    generic_replies = {"ok", "okay", "yes", "no", "thanks", "thank you", "hi", "hello"}

    if not message.strip() or message.strip().lower() in generic_replies:
        return False

    return 1 <= len(words) <= 6


def title_from_instruction(instruction: str) -> str:
    words = instruction.strip(" .").split()
    title = " ".join(words[:7]) or "AI Governance Policy"
    return title[:1].upper() + title[1:]


def tags_from_instruction(instruction: str) -> list[str]:
    lower_instruction = instruction.lower()
    tags = []
    for candidate in ("sales", "marketing", "healthcare", "finance", "brand-safety", "approval"):
        if candidate.replace("-", " ") in lower_instruction or candidate in lower_instruction:
            tags.append(candidate)
    return tags or ["ai-policy", "demo"]


def dsl_from_instruction(instruction: str) -> dict:
    lower_instruction = instruction.lower()
    field = "campaign_topic"
    operator = "contains"
    value = "marketing" if "marketing" in lower_instruction else "healthcare"
    action = "require_approval"

    if "sales" in lower_instruction:
        value = "sales"
    if "auto" in lower_instruction and "approve" in lower_instruction:
        action = "auto_approve"
    if "block" in lower_instruction or "unsupported" in lower_instruction:
        action = "flag_for_review"

    return {
        "conditions": [
            {
                "field": field,
                "operator": operator,
                "value": value,
            }
        ],
        "actions": [
            {
                "type": action,
                "value": "Human Reviewer" if action == "require_approval" else None,
            }
        ],
        "match_mode": "all",
        "stop_on_match": True,
    }


def policy_response(policy: PolicyPayload, policy_id: Optional[str] = None) -> dict:
    now = datetime.utcnow().isoformat()
    return {
        "id": policy_id or f"policy-{int(datetime.utcnow().timestamp())}",
        "name": policy.name,
        "description": policy.description,
        "summary": policy.description or policy.natural_language,
        "natural_language": policy.natural_language,
        "policy_type": policy.policy_type,
        "policy_scope": "base",
        "dsl": policy.dsl,
        "refined_instruction": policy.refined_instruction,
        "ai_instruction": policy.refined_instruction or policy.natural_language,
        "entity_name": policy.entity_name,
        "is_active": policy.is_active,
        "priority": policy.priority,
        "tags": policy.tags,
        "source": "demo",
        "created_at": now,
        "updated_at": now,
        "execution_count": 0,
        "last_executed_at": None,
    }


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    message = request.message.lower()

    if "status" in message or "agents" in message or "orchestrator" in message:
        result = await campaign_status()
        return ChatResponse(
            response="The orchestrator is online with 6 active agents.",
            tool_calls=[
                ToolCall(
                    id="tool-campaign-status",
                    name="campaign.status",
                    args={},
                    result=result,
                )
            ],
        )

    if "review" in message or "workbench" in message or "approval" in message:
        result = await workbench_reviews()
        review_count = len(result["reviews"])
        return ChatResponse(
            response=(
                f"There are {review_count} workbench items awaiting approval. "
                "Open Workbench to approve healthcare, sales marketing, and digital marketing review pauses."
            ),
            tool_calls=[
                ToolCall(
                    id="tool-workbench-reviews",
                    name="workbench.reviews",
                    args={},
                    result=result,
                )
            ],
        )

    if "policy" in message or "governance" in message or "violation" in message:
        result = await policy_events()
        return ChatResponse(
            response=(
                "Governance is active. Brand Safety flagged unsupported claims, "
                "and sales marketing discount claims require approval before publishing."
            ),
            tool_calls=[
                ToolCall(
                    id="tool-policies-events",
                    name="policies.events",
                    args={},
                    result=result,
                )
            ],
        )

    if "insight" in message or "roi" in message or "analytics" in message:
        result = await insights()
        return ChatResponse(
            response="Current demo insights: ROI is +28%, engagement is +18%, and 4 violations were prevented.",
            tool_calls=[
                ToolCall(
                    id="tool-insights",
                    name="insights.summary",
                    args={},
                    result=result,
                )
            ],
        )

    if "setting" in message or "notification" in message or "preference" in message:
        return ChatResponse(
            response=(
                "Settings are available from the left sidebar. For the demo, quick toggles update immediately "
                "for notifications, desktop alerts, weekly digest, and marketing emails."
            )
        )

    if (
        any(word in message for word in ("launch", "start", "run")) and "campaign" in message
    ) or looks_like_campaign_topic(request.message):
        topic = (
            extract_campaign_topic(request.message)
            if "campaign" in message
            else request.message.strip(" .")
        )
        result = await run_campaign(topic)
        return ChatResponse(
            response=(
                f"Campaign '{topic}' is running through the orchestration backend.\n"
                "Trend Analyzer, Deep Research, and Content Creator completed. "
                "Brand Safety found a governance issue, so Publisher is waiting for human approval in Workbench."
            ),
            tool_calls=[
                ToolCall(
                    id="tool-campaign-run",
                    name="campaign.run",
                    args={"topic": topic},
                    result=result,
                )
            ],
        )

    return ChatResponse(
        response=(
            "Ask me for a campaign topic like 'sales marketing', or ask for campaign status, "
            "workbench reviews, policy violations, ROI insights, or settings."
        )
    )


@router.post("/policies/analyze-input")
async def analyze_policy_input(request: PolicyInputRequest):
    instruction = request.input.strip()
    return {
        "suggested_type": "logical",
        "confidence": 0.91,
        "reason": "The rule has clear campaign governance conditions and review actions.",
        "suggested_name": title_from_instruction(instruction),
        "summary": f"Applies governance checks for: {instruction}",
        "dsl": dsl_from_instruction(instruction),
        "refined_instruction": (
            f"{instruction}. Flag unsupported claims, risky brand language, "
            "or missing approval evidence for human review."
        ),
        "entity_name": "campaign",
        "suggested_tags": tags_from_instruction(instruction),
    }


@router.post("/policies/check-conflicts")
async def check_policy_conflicts(request: PolicyConflictRequest):
    return {
        "conflicts": [],
        "overrides": [],
        "clarifications": [],
        "suggested_instructions": [
            "Require human review when claims lack supporting evidence.",
            "Pause publishing until Brand Safety clears the campaign.",
        ],
        "refined_instruction": (
            f"{request.natural_language}. Enforce Brand Safety review before publishing."
        ),
        "is_valid": True,
        "warnings": [],
    }


@router.post("/policies/translate")
async def translate_policy(request: PolicyTranslateRequest):
    return {
        "dsl": dsl_from_instruction(request.natural_language),
        "confidence": 0.9,
    }


@router.post("/policies/analyze")
async def analyze_policy(request: PolicyAnalyzeRequest):
    return {
        "conflicts": [],
        "overrides": [],
        "clarifications": [],
        "suggested_instructions": [
            f"{request.natural_language}. If evidence is missing, route to Workbench.",
            "Log the decision, responsible agent, and review reason.",
        ],
        "refined_instruction": (
            f"{request.natural_language}. Route exceptions to Workbench for approval."
        ),
        "is_valid": True,
        "warnings": [],
    }


@router.post("/policies")
async def create_policy(policy: PolicyPayload, db: Session = Depends(get_db)):
    # Minimal DB persistence: store rule_text + is_active.
    if policy.policy_type == "logical" and not policy.dsl:
        policy.dsl = dsl_from_instruction(policy.natural_language)

    rule_text = policy.refined_instruction or policy.natural_language

    p = PolicyModel(
        name=policy.name[:255],
        description=policy.description,
        rule_text=rule_text,
        status=PolicyStatus.passed,
        is_active=policy.is_active,
    )

    db.add(p)
    db.commit()
    db.refresh(p)

    # Return frontend-compatible response
    return policy_response(policy, str(p.id))



@router.get("/policies")
async def list_policies(db: Session = Depends(get_db)):
    policies = db.query(PolicyModel).order_by(PolicyModel.id.desc()).all()

    # Map DB model -> frontend Policy shape (best-effort)
    return [
        {
            "id": p.id,
            "name": p.rule_text[:60] if p.rule_text else f"Policy-{p.id}",
            "description": None,
            "natural_language": None,
            "summary": p.rule_text[:120] if p.rule_text else None,
            "policy_type": "logical",
            "policy_scope": "base",
            "dsl": None,
            "refined_instruction": None,
            "ai_instruction": None,
            "entity_name": None,
            "is_active": p.is_active,
            "priority": 50,
            "tags": [],
            "source": "db",
            "created_at": p.created_at.isoformat() if p.created_at else None,
            "updated_at": None,
            "execution_count": 0,
            "last_executed_at": None,
        }
        for p in policies
    ]


@router.delete("/policies/{policy_id}")
async def delete_policy(policy_id: int, db: Session = Depends(get_db)):
    p = db.query(PolicyModel).filter(PolicyModel.id == policy_id).first()
    if not p:
        return {"status": "not_found", "policy_id": policy_id}

    db.delete(p)
    db.commit()

    return {"status": "deleted", "policy_id": policy_id}




@router.patch("/policies/{policy_id}")
async def update_policy(policy_id: int, policy: PolicyPayload, db: Session = Depends(get_db)):
    # Minimal DB persistence: store rule_text + is_active.
    # Preserve existing response shape for frontend compatibility.
    p = db.query(PolicyModel).filter(PolicyModel.id == policy_id).first()
    if not p:
        return {"status": "not_found", "policy_id": policy_id}

    # Map frontend payload -> DB rule_text
    # Prefer refined_instruction if present; otherwise use natural_language.
    rule_text = policy.refined_instruction or policy.natural_language
    if policy.policy_type == "logical" and policy.dsl and not rule_text:
        rule_text = policy.natural_language

    p.rule_text = rule_text
    p.is_active = policy.is_active
    db.commit()

    return policy_response(policy, str(policy_id))


