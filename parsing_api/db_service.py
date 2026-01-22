"""Database service for Vercel serverless functions."""
import uuid
import os
from typing import Dict, Any
from datetime import datetime
from supabase import create_client, Client


class StorageService:
    """Service for uploading images to Supabase Storage."""
    
    def __init__(self):
        supabase_url = os.environ.get("SUPABASE_URL")
        supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
        self.client = create_client(supabase_url, supabase_key)
        self.bucket = os.environ.get("STORAGE_BUCKET", "question-images")
    
    async def upload_image(
        self, image_bytes: bytes, format: str, paper_id: str, 
        question_num: str, img_index: int
    ) -> str:
        """Upload an image to Supabase Storage."""
        filename = f"{paper_id}/{question_num}/img_{img_index}.{format}"
        
        self.client.storage.from_(self.bucket).upload(
            path=filename,
            file=image_bytes,
            file_options={"content-type": f"image/{format}"}
        )
        
        public_url = self.client.storage.from_(self.bucket).get_public_url(filename)
        return public_url


class DatabaseService:
    """Service for database operations via Supabase."""
    
    def __init__(self):
        supabase_url = os.environ.get("SUPABASE_URL")
        supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
        self.client = create_client(supabase_url, supabase_key)
        self.storage = StorageService()
    
    async def store_parsed_paper(
        self, parsed_data: Dict[str, Any], metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Store a complete parsed paper in the database."""
        paper_id = str(uuid.uuid4())
        title = metadata.get("title") or self._generate_title(metadata)
        
        paper_record = {
            "id": paper_id,
            "title": title,
            "exam_board": metadata["exam_board"],
            "subject": metadata.get("subject", "Economics"),
            "level": metadata.get("level", "A-Level"),
            "year": metadata["year"],
            "session": metadata["session"],
            "paper_number": metadata["paper_number"],
            "total_marks": metadata.get("total_marks"),
            "uploaded_at": datetime.utcnow().isoformat()
        }
        
        paper_response = self.client.table("Paper").insert(paper_record).execute()
        
        for question in parsed_data["questions"]:
            await self._store_question(paper_id, question)
        
        return paper_response.data[0] if paper_response.data else paper_record
    
    async def _store_question(self, paper_id: str, question_data: Dict[str, Any]):
        """Store a single question with its content."""
        question_id = str(uuid.uuid4())
        
        question_record = {
            "id": question_id,
            "paper_id": paper_id,
            "question_number": question_data["question_number"],
            "sequence_order": question_data["sequence_order"],
            "marks": question_data.get("marks")
        }
        
        self.client.table("Question").insert(question_record).execute()
        
        sequence = 0
        for content_item in question_data["content"]:
            await self._store_content(
                question_id, content_item, sequence,
                paper_id, question_data["question_number"]
            )
            sequence += 1
    
    async def _store_content(
        self, question_id: str, content_item: Dict[str, Any],
        sequence: int, paper_id: str, question_num: str
    ):
        """Store a content element (text or image)."""
        content_id = str(uuid.uuid4())
        content_type = content_item["type"]
        data = content_item["data"]
        
        content_record = {
            "id": content_id,
            "question_id": question_id,
            "sequence_order": sequence,
            "content_type": content_type
        }
        
        if content_type == "TEXT":
            content_record.update({
                "text": data["text"],
                "font_size": data.get("font_size"),
                "font_family": data.get("font_family"),
                "is_bold": data.get("is_bold", False),
                "is_italic": data.get("is_italic", False),
                "x": data.get("x"),
                "y": data.get("y"),
                "width": data.get("width"),
                "height": data.get("height")
            })
        elif content_type == "IMAGE":
            image_url = await self.storage.upload_image(
                image_bytes=data["image_bytes"],
                format=data["format"],
                paper_id=paper_id,
                question_num=question_num,
                img_index=data["img_index"]
            )
            
            content_record.update({
                "image_url": image_url,
                "image_width": data["width"],
                "image_height": data["height"],
                "x": data.get("x"),
                "y": data.get("y"),
                "width": data.get("bbox_width"),
                "height": data.get("bbox_height"),
                "alt_text": f"Image {data['img_index']} for question {question_num}"
            })
        
        self.client.table("QuestionContent").insert(content_record).execute()
    
    def _generate_title(self, metadata: Dict[str, Any]) -> str:
        """Generate a title from metadata."""
        return (
            f"{metadata['exam_board']} {metadata.get('subject', 'Economics')} "
            f"{metadata.get('level', 'A-Level')} Paper {metadata['paper_number']} - "
            f"{metadata['session']} {metadata['year']}"
        )
    
    async def get_paper(self, paper_id: str) -> Dict[str, Any]:
        """Retrieve a paper with all questions and content."""
        paper_response = self.client.table("Paper").select("*").eq("id", paper_id).execute()
        
        if not paper_response.data:
            raise ValueError(f"Paper {paper_id} not found")
        
        paper = paper_response.data[0]
        
        questions_response = (
            self.client.table("Question")
            .select("*")
            .eq("paper_id", paper_id)
            .order("sequence_order")
            .execute()
        )
        
        questions = []
        for question in questions_response.data:
            content_response = (
                self.client.table("QuestionContent")
                .select("*")
                .eq("question_id", question["id"])
                .order("sequence_order")
                .execute()
            )
            
            question["content"] = content_response.data
            questions.append(question)
        
        paper["questions"] = questions
        return paper
