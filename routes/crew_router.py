from fastapi import APIRouter, Depends

crew_router = APIRouter()

@crew_router.get("/crew")
async def get_crew():
    return {"message": "Crew information retrieved successfully."}