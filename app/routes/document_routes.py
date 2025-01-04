from flask import Blueprint, request, jsonify
from app.services.document_service import process_document

document_routes = Blueprint('document_routes', __name__)

@document_routes.route('/upload', methods=['POST'])
def upload_document():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    
    response = process_document(file)
    return jsonify(response)