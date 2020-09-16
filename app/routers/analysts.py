from fastapi import APIRouter, HTTPException
from typing import Optional

router = APIRouter()


@router.get("/api/analysts/search", tags = ["analysts"])
async def search_analyst(last_name: Optional[str] = None, first_name: Optional[str] = None, affiliation: Optional[str] = None):
    return {
        "last_name": "Cramer", 
        "first_name": "Jim",
        "affiliation": "CNBC"
        }