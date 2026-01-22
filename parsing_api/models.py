"""Pydantic models for API requests and responses."""
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class PaperMetadata(BaseModel):
    """Metadata for a past paper."""
    exam_board: str = Field(..., description="Exam board")
    subject: str = Field(default="Economics")
    level: str = Field(default="A-Level")
    year: int = Field(..., ge=2000, le=2030)
    session: str = Field(...)
    paper_number: int = Field(..., ge=1, le=3)
    total_marks: Optional[int] = None
    title: Optional[str] = None


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
    text: Optional[str] = None
    font_size: Optional[float] = None
    font_family: Optional[str] = None
    is_bold: bool = False
    is_italic: bool = False
    x: Optional[float] = None
    y: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
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
