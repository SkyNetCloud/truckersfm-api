import json
import time
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

# Import TruckersFM - make sure to install it first
try:
    from truckersfm import TruckersFM
    TFM_AVAILABLE = True
except ImportError:
    TFM_AVAILABLE = False
    print("Warning: truckersfm module not installed")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Allow CORS if needed
        if self.path == '/favicon.ico':
            self.send_response(404)
            self.end_headers()
            return
            
        if self.path != '/':
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'error': 'Endpoint not found. Use /'}
            self.wfile.write(json.dumps(response).encode())
            return
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        # Add CORS headers if needed
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        try:
            if not TFM_AVAILABLE:
                raise ImportError("truckersfm module not installed")
                
            tfm = TruckersFM()
            data = {
                'title': tfm.currentSongTitle(),
                'artist': tfm.currentSongArtist(),
                'albumart': tfm.currentSongAlbumArt(),
                'time': time.strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'success'
            }
        except Exception as e:
            data = {
                'error': str(e),
                'status': 'error',
                'time': time.strftime('%Y-%m-%d %H:%M:%S')
            }
        
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def log_message(self, format, *args):
        # Disable default logging to keep logs clean
        pass

def run_server():
    # Get port from environment variable (Render provides this)
    port = int(os.environ.get('PORT', 10000))
    host = '0.0.0.0'  # Important: Must be 0.0.0.0 for Render
    
    print(f"Starting server on {host}:{port}")
    print(f"API will be available at: http://{host}:{port}/")
    
    server = HTTPServer((host, port), Handler)
    server.serve_forever()

if __name__ == '__main__':
    run_server()