import os
import requests
from fastapi import APIRouter
from pydantic import BaseModel
from requests import RequestException

router = APIRouter(prefix="/campaign", tags=["Campaign"])

SUPERVITY_TOKEN = os.getenv("SUPERVITY_API_KEY")
ORCHESTRATOR_ID = os.getenv("ORCHESTRATOR_ID")
ENABLE_SUPERVITY = os.getenv("ENABLE_SUPERVITY", "false").lower() == "true"
SUPERVITY_VERIFY_SSL = os.getenv("SUPERVITY_VERIFY_SSL", "true").lower() != "false"
SUPERVITY_API_URL = os.getenv(
    "SUPERVITY_API_URL",
    "https://auto-workflow-api.supervity.ai",
).rstrip("/")
SUPERVITY_URL = f"{SUPERVITY_API_URL}/api/v1/workflow-runs/execute/stream"


class CampaignRunRequest(BaseModel):
    campaign: str | None = None
    topic: str | None = None

    def resolve_topic(self) -> str:
        return self.campaign or self.topic or ""


@router.post("/run")
async def run_campaign(request: CampaignRunRequest):
    topic = request.resolve_topic()
    if not topic:
        return {
            "status": "error",
            "message": "Please provide a campaign name via 'campaign' or 'topic'."
        }
    supervity_response = "Supervity not configured; using demo orchestration."
    supervity_status_code = None

    if ENABLE_SUPERVITY and SUPERVITY_TOKEN and ORCHESTRATOR_ID:
        try:
            response = requests.post(
                SUPERVITY_URL,
                headers={
                    "Authorization": f"Bearer {SUPERVITY_TOKEN}",
                    "x-source": "v1",
                },
                data={
                    "workflowId": ORCHESTRATOR_ID,
                    "inputs[campaign_id]": topic,
                },
                timeout=300,
                verify=SUPERVITY_VERIFY_SSL,
            )
            supervity_status_code = response.status_code
            supervity_response = response.text[:5000]
        except RequestException as e:
            supervity_response = f"Supervity unavailable; using demo orchestration. {e}"

    return {
        "status": "success",
        "campaign": topic,
        "agents": [
            {
                "name": "Trend Analyzer",
                "status": "completed"
            },
            {
                "name": "Deep Research",
                "status": "completed"
            },
            {
                "name": "Content Creator",
                "status": "completed"
            },
            {
                "name": "Brand Safety",
                "status": "warning"
            },
            {
                "name": "Publisher",
                "status": "waiting_approval"
            },
            {
                "name": "ROI Optimizer",
                "status": "active"
            }
        ],
        "timeline": [
            "Trend detected",
            "Audience research completed",
            "Campaign content generated",
            "Brand safety violation detected",
            "Workflow paused for review"
        ],
        "workbench": {
            "required": True,
            "reason": "Unsupported healthcare statistic"
        },
        "supervity_connected": bool(supervity_status_code and supervity_status_code < 400),
        "supervity_status_code": supervity_status_code,
        "supervity_response": supervity_response
    }


@router.get("/status")
async def campaign_status():
    return {
        "status": "online",

        "agents_running": 6,

        "orchestrator_id": ORCHESTRATOR_ID,

        "active_agents": [
            "Trend Analyzer",
            "Deep Research",
            "Content Creator",
            "Brand Safety",
            "Publisher",
            "ROI Optimizer"
        ]
    }

