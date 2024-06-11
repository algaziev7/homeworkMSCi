from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.services.osv_query import query_osv_api

router = APIRouter()

@router.get("/versions")
async def get_versions(name: str):
    try:
        versions = await query_osv_api(name)

        if not versions:
            return {
                "name": name,
                "versions": [],
                "timestamp": datetime.now().isoformat(),
                "message": "No vulnerable versions found for the specified package"
            }

        return {
            "name": name,
            "versions": versions,
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
