"""Supabase storage utilities for uploading images."""
import uuid
from typing import Dict, Any
from supabase import create_client, Client
from app.config import get_settings


class StorageService:
    """Service for managing file uploads to Supabase Storage."""
    
    def __init__(self):
        """Initialize Supabase client."""
        settings = get_settings()
        self.client: Client = create_client(
            settings.supabase_url,
            settings.supabase_service_key  # Use service key for admin access
        )
        self.bucket = settings.storage_bucket
    
    async def upload_image(
        self, 
        image_bytes: bytes, 
        format: str,
        paper_id: str,
        question_num: str,
        img_index: int
    ) -> str:
        """
        Upload an image to Supabase Storage.
        
        Args:
            image_bytes: Image data as bytes
            format: Image format (jpg, png, etc.)
            paper_id: Paper UUID for organizing
            question_num: Question number
            img_index: Image index within question
            
        Returns:
            Public URL of uploaded image
        """
        # Generate unique filename
        filename = f"{paper_id}/{question_num}/img_{img_index}.{format}"
        
        try:
            # Upload to Supabase Storage
            response = self.client.storage.from_(self.bucket).upload(
                path=filename,
                file=image_bytes,
                file_options={"content-type": f"image/{format}"}
            )
            
            # Get public URL
            public_url = self.client.storage.from_(self.bucket).get_public_url(filename)
            
            return public_url
            
        except Exception as e:
            print(f"Error uploading image {filename}: {e}")
            raise
    
    def ensure_bucket_exists(self) -> bool:
        """
        Ensure the storage bucket exists, create if it doesn't.
        
        Returns:
            True if bucket exists or was created
        """
        try:
            # Try to get bucket
            buckets = self.client.storage.list_buckets()
            bucket_names = [b.name for b in buckets]
            
            if self.bucket not in bucket_names:
                # Create bucket
                self.client.storage.create_bucket(
                    self.bucket,
                    options={"public": True}  # Make images publicly accessible
                )
                print(f"Created storage bucket: {self.bucket}")
            
            return True
            
        except Exception as e:
            print(f"Error ensuring bucket exists: {e}")
            return False
