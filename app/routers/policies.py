from fastapi import APIRouter

router = APIRouter(tags=["Policies"])


@router.get("/policies/events")
async def policy_events():
    return {
        "violations": [
            {
                "campaign": "AI in Healthcare",
                "policy": "No unsupported claims",
                "severity": "high",
                "agent": "Brand Safety"
            }
        ]
    }

