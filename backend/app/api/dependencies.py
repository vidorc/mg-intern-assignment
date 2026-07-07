from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal
from app.clients.setu_client import SetuClient
from app.repositories.signature_repo import SignatureRepository
from app.services.signature_service import SignatureService

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def get_setu_client():
    client = SetuClient()
    try:
        yield client
    finally:
        await client.close()

async def get_repository(session: AsyncSession = Depends(get_db)) -> SignatureRepository:
    return SignatureRepository(session)

async def get_service(
    client: SetuClient = Depends(get_setu_client),
    repo: SignatureRepository = Depends(get_repository),
) -> SignatureService:
    return SignatureService(client, repo)
