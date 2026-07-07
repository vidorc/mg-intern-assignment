import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from app.core.config import settings
from app.core.logging import logger

class SetuClient:
    def __init__(self):
        self.base_url = str(settings.setu_base_url)
        self.headers = {
            "x-client-id": settings.setu_client_id.get_secret_value(),
            "x-client-secret": settings.setu_client_secret.get_secret_value(),
            "x-product-instance-id": settings.setu_product_instance_id.get_secret_value(),
        }
        self.client = httpx.AsyncClient(timeout=30.0)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def upload_document(self, file_content: bytes, filename: str) -> str:
        logger.info("Uploading document to Setu")
        files = {"file": (filename, file_content, "application/pdf")}
        response = await self.client.post(f"{self.base_url}/documents", headers=self.headers, files=files)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Document uploaded: {data['id']}")
        return data["id"]

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def create_signature(self, document_id: str) -> dict:
        payload = {
            "documentId": document_id,
            "redirectUrl": str(settings.redirect_url),
            "signers": [{"name": "Signer", "email": "signer@example.com"}],
        }
        logger.info("Creating signature request")
        response = await self.client.post(f"{self.base_url}/signature", headers=self.headers, json=payload)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Signature created: {data['id']}")
        return {"signatureId": data["id"], "signerUrl": data["signerUrl"]}

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def get_signature_status(self, signature_id: str) -> dict:
        response = await self.client.get(f"{self.base_url}/signature/{signature_id}", headers=self.headers)
        response.raise_for_status()
        return response.json()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def download_document(self, document_id: str) -> bytes:
        response = await self.client.get(f"{self.base_url}/documents/{document_id}/download", headers=self.headers)
        response.raise_for_status()
        return response.content

    async def close(self):
        await self.client.aclose()
