from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.schemas.response import ApiResponse, UploadResponseData
from app.services.signature_service import SignatureService
from app.api.dependencies import get_service
from app.utils.rate_limit import limiter
from app.core.logging import logger

router = APIRouter()

@router.post("/upload-contract", response_model=ApiResponse)
@limiter.limit("5/minute")
async def upload_contract(
    request: Request,
    file: UploadFile = File(...),
    service: SignatureService = Depends(get_service),
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (max 5MB)")
    try:
        db_req = await service.process_upload(content, file.filename)
        data = UploadResponseData(
            documentId=db_req.document_id,
            signatureId=db_req.signature_id,
            signerUrl=db_req.signer_url,
            status=db_req.status,
        )
        return ApiResponse(success=True, message="Uploaded and signature created", data=data.dict())
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
