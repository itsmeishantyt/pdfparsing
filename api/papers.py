"""
Vercel serverless function for retrieving papers.
"""
from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsing_api.db_service import DatabaseService


class handler(BaseHTTPRequestHandler):
    """Vercel serverless function handler."""
    
    def do_GET(self):
        """Handle GET request for paper retrieval."""
        try:
            # Extract paper_id from path
            # Path format: /api/papers/PAPER_ID
            path_parts = self.path.split('/')
            
            if len(path_parts) < 4:
                self.send_error_response(400, "Paper ID required")
                return
            
            paper_id = path_parts[3].split('?')[0]  # Remove query params if present
            
            # Get paper from database
            db_service = DatabaseService()
            paper = db_service.get_paper_sync(paper_id)
            
            if not paper:
                self.send_error_response(404, f"Paper {paper_id} not found")
                return
            
            # Send success response
            self.send_success_response(paper)
            
        except ValueError as e:
            self.send_error_response(404, str(e))
        except Exception as e:
            self.send_error_response(500, f"Error retrieving paper: {str(e)}")
    
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
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
