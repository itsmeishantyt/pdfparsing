"""
Vercel serverless function for PDF upload and parsing.
"""
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import time
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsing_api.pdf_parser import PDFParser
from parsing_api.db_service import DatabaseService
from parsing_api.models import PaperMetadata, ParseResponse

app = FastAPI()

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/upload", response_model=ParseResponse)
async def upload_and_parse_pdf(
    file: UploadFile = File(..., description="PDF file to parse"),
    metadata: str = Form(..., description="Paper metadata as JSON string")
):
    """Upload and parse a PDF past paper."""
    
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")
    
    try:
        metadata_dict = json.loads(metadata)
        paper_metadata = PaperMetadata(**metadata_dict)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in metadata")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid metadata: {str(e)}")
    
    try:
        start_time = time.time()
        
        pdf_bytes = await file.read()
        
        parser = PDFParser()
        parsed_data = parser.parse_pdf(pdf_bytes)
        
        db_service = DatabaseService()
        paper = await db_service.store_parsed_paper(
            parsed_data=parsed_data,
            metadata=paper_metadata.dict()
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
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "PDF Parsing API"}
