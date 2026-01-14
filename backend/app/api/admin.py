from fastapi import APIRouter

router = APIRouter()


@router.post("/seed")
async def seed_placeholder():
    return {"status": "not_implemented"}

