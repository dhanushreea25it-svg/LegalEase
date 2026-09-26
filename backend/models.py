from pydantic import BaseModel


class DocumentRequest(BaseModel):
    """
    Request model for generating a legal document.
    """

    document_type: str
    parties: str
    terms: str
    effective_date: str


class DocumentResponse(BaseModel):
    """
    Response model containing the generated document.
    """

    document_type: str
    content: str