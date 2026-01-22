"""
Vercel serverless function for retrieving papers.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsing_api.db_service import DatabaseService
from parsing_api.models import PaperResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/papers/{paper_id}", response_model=PaperResponse)
async def get_paper(paper_id: str):
    """Retrieve a parsed paper with all questions and content."""
    
    try:
        db_service = DatabaseService()
        paper = await db_service.get_paper(paper_id)
        return paper
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving paper: {str(e)}")
