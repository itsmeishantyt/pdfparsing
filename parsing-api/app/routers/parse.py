"""API router for PDF parsing endpoints."""
import time
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Dict, Any
import json

from app.models.request import PaperMetadata
from app.models.response import ParseResponse, PaperResponse
from app.services.pdf_parser import PDFParser
from app.services.db_service import DatabaseService


router = APIRouter(prefix="/api", tags=["parsing"])


@router.post("/upload", response_model=ParseResponse)
async def upload_and_parse_pdf(
    file: UploadFile = File(..., description="PDF file to parse"),
    metadata: str = Form(..., description="Paper metadata as JSON string")
):
    """
    Upload and parse a PDF past paper.
    
    Args:
        file: PDF file
        metadata: JSON string with paper metadata
        
    Returns:
        Parse result with paper ID and statistics
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")
    
    # Parse metadata
    try:
        metadata_dict = json.loads(metadata)
        paper_metadata = PaperMetadata(**metadata_dict)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in metadata")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid metadata: {str(e)}")
    
    try:
        start_time = time.time()
        
        # Read PDF bytes
        pdf_bytes = await file.read()
        
        # Parse PDF
        parser = PDFParser()
        parsed_data = parser.parse_pdf(pdf_bytes)
        
        # Store in database
        db_service = DatabaseService()
        paper = await db_service.store_parsed_paper(
            parsed_data=parsed_data,
            metadata=paper_metadata.model_dump()
        )
        
        processing_time = time.time() - start_time
        
        return ParseResponse(
            paper_id=paper["id"],
            status="success",
            questions_count=len(parsed_data["questions"]),
            processing_time=round(processing_time, 2),
            message=f"Successfully parsed {len(parsed_data['questions'])} questions"
        )
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"CRITICAL ERROR: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing PDF: {str(e)}"
        )


@router.get("/papers/{paper_id}", response_model=PaperResponse)
async def get_paper(paper_id: str):
    """
    Retrieve a parsed paper with all questions and content.
    
    Args:
        paper_id: Paper UUID
        
    Returns:
        Complete paper data
    """
    try:
        db_service = DatabaseService()
        paper = await db_service.get_paper(paper_id)
        return paper
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving paper: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "PDF Parsing API"}
