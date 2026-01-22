"""
Vercel serverless function for PDF upload and parsing.
"""
from http.server import BaseHTTPRequestHandler
import json
import time
import sys
import os
import cgi
from io import BytesIO

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsing_api.pdf_parser import PDFParser
from parsing_api.db_service import DatabaseService


class handler(BaseHTTPRequestHandler):
    """Vercel serverless function handler."""
    
    def do_POST(self):
        """Handle POST request for PDF upload."""
        try:
            # Parse multipart form data
            content_type = self.headers.get('Content-Type', '')
            
            if 'multipart/form-data' not in content_type:
                self.send_error_response(400, "Content-Type must be multipart/form-data")
                return
            
            # Parse form data
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
            
            # Get file and metadata
            if 'file' not in form:
                self.send_error_response(400, "No file provided")
                return
            
            if 'metadata' not in form:
                self.send_error_response(400, "No metadata provided")
                return
            
            file_item = form['file']
            metadata_str = form['metadata'].value
            
            # Validate PDF
            if not file_item.filename.endswith('.pdf'):
                self.send_error_response(400, "Only PDF files are accepted")
                return
            
            # Parse metadata
            try:
                metadata = json.loads(metadata_str)
            except json.JSONDecodeError:
                self.send_error_response(400, "Invalid JSON in metadata")
                return
            
            # Process PDF
            start_time = time.time()
            
            pdf_bytes = file_item.file.read()
            
            parser = PDFParser()
            parsed_data = parser.parse_pdf(pdf_bytes)
            
            # Store in database (synchronous version)
            db_service = DatabaseService()
            paper = db_service.store_parsed_paper_sync(
                parsed_data=parsed_data,
                metadata=metadata
            )
            
            processing_time = time.time() - start_time
            
            # Send success response
            response_data = {
                "paperId": paper["id"],
                "status": "success",
                "questionsCount": len(parsed_data["questions"]),
                "processingTime": round(processing_time, 2),
                "message": f"Successfully parsed {len(parsed_data['questions'])} questions"
            }
            
            self.send_success_response(response_data)
            
        except Exception as e:
            self.send_error_response(500, f"Error processing PDF: {str(e)}")
    
    def send_success_response(self, data):
        """Send JSON success response."""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def send_error_response(self, code, message):
        """Send JSON error response."""
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        error_data = {"detail": message}
        self.wfile.write(json.dumps(error_data).encode())
    
    def do_OPTIONS(self):
        """Handle OPTIONS request for CORS preflight."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
