"""Request models for API endpoints."""
from pydantic import BaseModel, Field
from typing import Optional


class PaperMetadata(BaseModel):
    """Metadata for a past paper."""
    
    exam_board: str = Field(..., alias="examBoard", description="Exam board (e.g., AQA, Edexcel, OCR)")
    subject: str = Field(default="Economics", description="Subject name")
    level: str = Field(default="A-Level", description="Level (e.g., A-Level, GCSE)")
    year: int = Field(..., description="Year of the exam", ge=2000, le=2030)
    session: str = Field(..., description="Session (e.g., June, November)")
    paper_number: int = Field(..., alias="paperNumber", description="Paper number (1, 2, 3)", ge=1, le=3)
    total_marks: Optional[int] = Field(None, alias="totalMarks", description="Total marks for the paper")
    title: Optional[str] = Field(None, description="Custom title for the paper")
