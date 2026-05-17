from fastapi import APIRouter

router = APIRouter(tags=["Workbench"])


@router.get("/workbench/reviews")
async def workbench_reviews():
    return {
        "reviews": [
            {
                "id": "review-001",
                "campaign": "AI in Healthcare",
                "issue": "Unsupported healthcare statistic",
                "status": "Awaiting Approval",
                "severity": "high",
                "agent": "Brand Safety"
            },
            {
                "id": "review-002",
                "campaign": "Sales Marketing",
                "issue": "Discount claim needs manager approval",
                "status": "Awaiting Approval",
                "severity": "medium",
                "agent": "Publisher"
            },
            {
                "id": "review-003",
                "campaign": "Digital Marketing",
                "issue": "Audience targeting requires policy confirmation",
                "status": "Awaiting Approval",
                "severity": "medium",
                "agent": "ROI Optimizer"
            }
        ]
    }


@router.post("/workbench/approve")
async def approve_review(review_id: str):
    return {
        "status": "approved",
        "review_id": review_id,
        "workflow": "resumed"
    }

