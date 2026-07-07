from fastapi import APIRouter, Depends, HTTPException
from app.schemas.response import ApiResponse, StatusResponseData
from app.services.signature_service import SignatureService
from app.api.dependencies import get_service

router = APIRouter()

@router.get("/signature-status/{signature_id}", response_model=ApiResponse)
async def signature_status(
    signature_id: str,
    service: SignatureService = Depends(get_service),
):
    db_req = await service.get_signature_status(signature_id)
    if not db_req:
        raise HTTPException(status_code=404, detail="Signature request not found")
    data = StatusResponseData(
        signatureId=db_req.signature_id,
        status=db_req.status,
        documentId=db_req.document_id,
        signerUrl=db_req.signer_url,
    )
    return ApiResponse(success=True, message="Status retrieved", data=data.dict())
