from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.signature import SignatureRequest

class SignatureRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def get_all(self, limit: int = 20) -> list:
        result = await self.session.execute(select(SignatureRequest).order_by(SignatureRequest.created_at.desc()).limit(limit))
        return result.scalars().all()

    async def create(self, document_id: str, signature_id: str, signer_url: str) -> SignatureRequest:
        req = SignatureRequest(
            document_id=document_id,
            signature_id=signature_id,
            signer_url=signer_url,
        )
        self.session.add(req)
        await self.session.commit()
        await self.session.refresh(req)
        return req

    async def get_by_signature_id(self, signature_id: str) -> Optional[SignatureRequest]:
        result = await self.session.execute(
            select(SignatureRequest).where(SignatureRequest.signature_id == signature_id)
        )
        return result.scalar_one_or_none()

    async def update_status(self, signature_id: str, status: str) -> None:
        req = await self.get_by_signature_id(signature_id)
        if req:
            req.status = status
            await self.session.commit()
