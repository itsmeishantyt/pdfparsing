"""Response models for API endpoints."""
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class ContentType(str, Enum):
    """Types of content within a question."""
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    TABLE = "TABLE"
    DIAGRAM = "DIAGRAM"
    EQUATION = "EQUATION"


class QuestionContentResponse(BaseModel):
    """Response model for question content elements."""
    
    id: str
    sequence_order: int
    content_type: ContentType
    
    # Text content
    text: Optional[str] = None
    font_size: Optional[float] = None
    font_family: Optional[str] = None
    is_bold: bool = False
    is_italic: bool = False
    
    # Layout
    x: Optional[float] = None
    y: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    
    # Image content
    image_url: Optional[str] = None
    image_width: Optional[int] = None
    image_height: Optional[int] = None
    alt_text: Optional[str] = None


class QuestionResponse(BaseModel):
    """Response model for a question."""
    
    id: str
    question_number: str
    sequence_order: int
    marks: Optional[int] = None
    content: List[QuestionContentResponse]


class PaperResponse(BaseModel):
    """Response model for a paper."""
    
    id: str
    title: str
    exam_board: str
    subject: str
    level: str
    year: int
    session: str
    paper_number: int
    total_marks: Optional[int] = None
    uploaded_at: str
    questions: List[QuestionResponse] = []


class ParseResponse(BaseModel):
    """Response model for PDF parsing operation."""
    
    paper_id: str
    status: str
    questions_count: int
    processing_time: float
    message: Optional[str] = None
