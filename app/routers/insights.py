from fastapi import APIRouter

router = APIRouter(tags=["Insights"])


@router.get("/insights")
async def insights():
    return {
        "roi": "+28%",
        "engagement": "+18%",
        "violations_prevented": 4,
        "campaigns_reviewed": 12
    }
