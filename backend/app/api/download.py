from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from app.services.signature_service import SignatureService
from app.api.dependencies import get_service
import io

router = APIRouter()

@router.get("/download/{signature_id}")
async def download_signed_document(
    signature_id: str,
    service: SignatureService = Depends(get_service),
):
    content = await service.download_if_signed(signature_id)
    if content is None:
        raise HTTPException(status_code=400, detail="Document not signed or not found")
    return StreamingResponse(
        io.BytesIO(content),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=signed_{signature_id}.pdf"}
    )
