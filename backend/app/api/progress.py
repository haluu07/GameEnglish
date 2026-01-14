from fastapi import APIRouter

router = APIRouter()


@router.get("/me/progress")
async def progress_placeholder():
    return {"unlocked_mission_ids": [], "best_scores": {}, "xp_total": 0, "streak_count": 0}

