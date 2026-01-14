from fastapi import APIRouter

router = APIRouter()


@router.get("/placeholder")
async def auth_placeholder():
    return {"message": "auth endpoints will be implemented"}

