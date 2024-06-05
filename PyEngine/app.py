from flask import Flask, send_from_directory
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='static')

# Serve the main page
@app.route('/')
def serve_vue_app():
    return send_from_directory(app.static_folder, 'index.html')

# Serve static files (CSS, JS, images, etc.)
@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

# Handle all other routes and fallback to index.html for Vue router to handle
@app.errorhandler(404)
def page_not_found(e):
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    host_address = os.getenv('ServerAddress')  # Default to 127.0.0.1 if not set
    app.run(host=host_address, port=80)
