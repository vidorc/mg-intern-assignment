from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal
from app.clients.setu_client import SetuClient
from app.api.dependencies import get_setu_client

router = APIRouter()

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.get("/ready")
async def ready(db: AsyncSession = Depends(lambda: AsyncSessionLocal())):
    try:
        await db.execute("SELECT 1")
        return {"status": "ready", "database": "connected"}
    except Exception as e:
        return {"status": "not ready", "database": str(e)}

@router.get("/live")
async def live(client: SetuClient = Depends(get_setu_client)):
    try:
        # simple check – maybe call a lightweight endpoint
        await client.client.get(f"{client.base_url}/documents", headers=client.headers)
        return {"status": "live", "setu": "connected"}
    except Exception as e:
        return {"status": "not live", "setu": str(e)}
