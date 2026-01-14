from fastapi import APIRouter

router = APIRouter()


@router.get("/levels")
async def list_levels_placeholder():
    return []

