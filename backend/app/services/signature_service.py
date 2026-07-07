from app.clients.setu_client import SetuClient
from app.repositories.signature_repo import SignatureRepository
from app.core.logging import logger

class SignatureService:
    def __init__(self, client: SetuClient, repo: SignatureRepository):
        self.client = client
        self.repo = repo

    async def process_upload(self, file_content: bytes, filename: str):
        document_id = await self.client.upload_document(file_content, filename)
        sig_result = await self.client.create_signature(document_id)
        db_req = await self.repo.create(
            document_id=document_id,
            signature_id=sig_result["signatureId"],
            signer_url=sig_result["signerUrl"],
        )
        logger.info(f"Stored signature request {db_req.signature_id}")
        return db_req

    async def get_signature_status(self, signature_id: str):
        db_req = await self.repo.get_by_signature_id(signature_id)
        if not db_req:
            return None
        # Sync with Setu
        setu_data = await self.client.get_signature_status(signature_id)
        await self.repo.update_status(signature_id, setu_data.get("status", "UNKNOWN"))
        return db_req

    async def download_if_signed(self, signature_id: str):
        db_req = await self.repo.get_by_signature_id(signature_id)
        if not db_req or db_req.status != "SIGNED":
            return None
        return await self.client.download_document(db_req.document_id)
