import uuid
from app.core.config import settings

class MockSetuClient:
    def __init__(self):
        self._store = {}

    async def upload_document(self, file_content: bytes, filename: str) -> str:
        doc_id = str(uuid.uuid4())
        print(f"[MOCK] Uploaded document → {doc_id}")
        return doc_id

    async def create_signature(self, document_id: str) -> dict:
        sig_id = str(uuid.uuid4())
        signer_url = f"{settings.redirect_url}?mock_signature_id={sig_id}"
        self._store[sig_id] = "PENDING"
        print(f"[MOCK] Created signature {sig_id} for document {document_id}")
        return {"signatureId": sig_id, "signerUrl": signer_url}

    async def get_signature_status(self, signature_id: str) -> dict:
        self._store[signature_id] = "SIGNED"
        return {"status": "SIGNED"}

    async def download_document(self, document_id: str) -> bytes:
        pdf = (
            b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
            b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
            b"3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R/Resources<<>>>>endobj\n"
            b"xref\n0 4\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n"
            b"trailer<</Size 4/Root 1 0 R>>\nstartxref\n190\n%%EOF"
        )
        return pdf

    async def close(self):
        self._store.clear()

SetuClient = MockSetuClient
