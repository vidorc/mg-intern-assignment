from pydantic import BaseModel

class ApiResponse(BaseModel):
    success: bool
    message: str
    data: dict | None = None

class UploadResponseData(BaseModel):
    documentId: str
    signatureId: str
    signerUrl: str
    status: str

class StatusResponseData(BaseModel):
    signatureId: str
    status: str
    documentId: str
    signerUrl: str

# We'll use ApiResponse wrapper in endpoints
