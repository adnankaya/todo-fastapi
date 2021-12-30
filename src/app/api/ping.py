from fastapi import APIRouter

router = APIRouter()


@router.get("/async-ping")
async def pong():
    # some async operation could happen here
    # example: `notes = await get_all_notes()`
    return {"async-ping": "async-pong"}
