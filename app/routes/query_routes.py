from flask import Blueprint, request, jsonify
from app.services.query_service import handle_query

query_routes = Blueprint('query_routes', __name__)

@query_routes.route('/search', methods=['POST'])
def search_query():
    query = request.json.get('query')
    if not query:
        return jsonify({"error": "Query is required"}), 400
    
    response = handle_query(query)
    return jsonify(response)