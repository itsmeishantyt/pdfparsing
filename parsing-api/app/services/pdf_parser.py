"""Core PDF parsing service using PyMuPDF."""
import fitz  # PyMuPDF
import io
import re
from PIL import Image
from typing import List, Dict, Any, Tuple
from datetime import datetime


class PDFParser:
    """Parser for extracting content from PDF past papers."""
    
    def __init__(self):
        """Initialize the PDF parser."""
        # Question number pattern: matches "1", "2a", "2b(i)", "3(c)(ii)", etc.
        self.question_pattern = re.compile(
            r'^(\d+)(\s*\([a-z]\))?(\s*\([ivxIVX]+\))?\s*'
        )
    
    def parse_pdf(self, pdf_bytes: bytes) -> Dict[str, Any]:
        """
        Parse a PDF and extract all content with layout preservation.
        
        Args:
            pdf_bytes: PDF file as bytes
            
        Returns:
            Dictionary containing parsed pages, images, and metadata
        """
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        parsed_data = {
            "metadata": self._extract_metadata(doc),
            "pages": [],
            "all_images": [],
            "questions": []
        }
        
        # Parse each page
        for page_num in range(len(doc)):
            page = doc[page_num]
            page_data = self._parse_page(page, page_num)
            parsed_data["pages"].append(page_data)
        
        # Segment into questions
        parsed_data["questions"] = self._segment_questions(parsed_data["pages"])
        
        doc.close()
        return parsed_data
    
    def _extract_metadata(self, doc: fitz.Document) -> Dict[str, Any]:
        """Extract metadata from PDF."""
        metadata = doc.metadata
        return {
            "page_count": len(doc),
            "title": metadata.get("title", ""),
            "author": metadata.get("author", ""),
            "subject": metadata.get("subject", ""),
            "creator": metadata.get("creator", "")
        }
    
    def _parse_page(self, page: fitz.Page, page_num: int) -> Dict[str, Any]:
        """
        Parse a single page and extract text and images with positions.
        
        Args:
            page: PyMuPDF page object
            page_num: Page number (0-indexed)
            
        Returns:
            Dictionary with page content
        """
        # Get page dimensions
        page_rect = page.rect
        
        # Extract text with detailed formatting
        text_elements = self._extract_text_with_formatting(page)
        
        # Extract images
        image_elements = self._extract_images(page, page_num)
        
        return {
            "page_number": page_num + 1,
            "width": page_rect.width,
            "height": page_rect.height,
            "text_elements": text_elements,
            "image_elements": image_elements
        }
    
    def _extract_text_with_formatting(self, page: fitz.Page) -> List[Dict[str, Any]]:
        """
        Extract text with font, size, position, and formatting info.
        
        Args:
            page: PyMuPDF page object
            
        Returns:
            List of text elements with formatting
        """
        text_elements = []
        
        # Get text as dictionary with detailed formatting
        blocks = page.get_text("dict", flags=11)["blocks"]
        
        for block in blocks:
            # Only process text blocks (type 0)
            if block.get("type") != 0:
                continue
            
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    # Get bounding box
                    bbox = span["bbox"]  # [x0, y0, x1, y1]
                    
                    # Determine font styling
                    flags = span.get("flags", 0)
                    is_bold = bool(flags & 2**4)  # Bit 4 indicates bold
                    is_italic = bool(flags & 2**1)  # Bit 1 indicates italic
                    
                    text_elements.append({
                        "text": span["text"],
                        "font_family": span.get("font", "unknown"),
                        "font_size": round(span.get("size", 12), 2),
                        "is_bold": is_bold,
                        "is_italic": is_italic,
                        "color": span.get("color", 0),
                        "x": round(bbox[0], 2),
                        "y": round(bbox[1], 2),
                        "width": round(bbox[2] - bbox[0], 2),
                        "height": round(bbox[3] - bbox[1], 2)
                    })
        
        return text_elements
    
    def _extract_images(self, page: fitz.Page, page_num: int) -> List[Dict[str, Any]]:
        """
        Extract images from a page with position and metadata.
        
        Args:
            page: PyMuPDF page object
            page_num: Page number for naming
            
        Returns:
            List of image data dictionaries
        """
        image_elements = []
        image_list = page.get_images()
        
        for img_index, img_info in enumerate(image_list):
            try:
                xref = img_info[0]
                
                # Extract image
                base_image = page.parent.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                # Get image position on page
                # This gets all rectangles where this image appears
                rects = page.get_image_rects(xref)
                
                if rects:
                    bbox = rects[0]  # Use first occurrence
                    
                    # Load image to get dimensions
                    pil_image = Image.open(io.BytesIO(image_bytes))
                    
                    image_elements.append({
                        "image_bytes": image_bytes,
                        "format": image_ext,
                        "width": pil_image.width,
                        "height": pil_image.height,
                        "x": round(bbox.x0, 2),
                        "y": round(bbox.y0, 2),
                        "bbox_width": round(bbox.width, 2),
                        "bbox_height": round(bbox.height, 2),
                        "xref": xref,
                        "page_num": page_num,
                        "img_index": img_index
                    })
            except Exception as e:
                # Skip problematic images
                print(f"Warning: Could not extract image {img_index} on page {page_num}: {e}")
                continue
        
        return image_elements
    
    def _segment_questions(self, pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Segment pages into individual questions.
        
        Uses pattern matching to identify question numbers and group content.
        
        Args:
            pages: List of parsed page data
            
        Returns:
            List of questions with their content
        """
        questions = []
        current_question = None
        sequence_order = 0
        
        for page in pages:
            for element in page["text_elements"]:
                text = element["text"].strip()
                
                # Check if this looks like a question number
                match = self.question_pattern.match(text)
                
                # Must be a match and reasonably sized (not tiny text)
                if match and element["font_size"] >= 9:
                    # Save previous question
                    if current_question:
                        questions.append(current_question)
                        sequence_order += 1
                    
                    # Start new question
                    question_number = match.group(0).strip()
                    current_question = {
                        "question_number": question_number,
                        "sequence_order": sequence_order,
                        "marks": self._extract_marks(text),
                        "content": [],
                        "page_number": page["page_number"]
                    }
                
                # Add content to current question
                if current_question:
                    current_question["content"].append({
                        "type": "TEXT",
                        "data": element
                    })
            
            # Add images from this page to current question
            if current_question:
                for img_element in page["image_elements"]:
                    current_question["content"].append({
                        "type": "IMAGE",
                        "data": img_element
                    })
        
        # Don't forget the last question
        if current_question:
            questions.append(current_question)
        
        return questions
    
    def _extract_marks(self, text: str) -> int:
        """
        Extract mark allocation from question text.
        
        Looks for patterns like [6 marks], (4 marks), [3], etc.
        
        Args:
            text: Question text
            
        Returns:
            Number of marks, or None if not found
        """
        # Pattern: [6 marks], (4 marks), [3], (5), etc.
        mark_patterns = [
            r'\[(\d+)\s*marks?\]',
            r'\((\d+)\s*marks?\)',
            r'\[(\d+)\]',
            r'\((\d+)\)'
        ]
        
        for pattern in mark_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    return int(match.group(1))
                except (ValueError, IndexError):
                    continue
        
        return None
