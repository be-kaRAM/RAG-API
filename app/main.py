import os
from flask import Flask
from app.routes.document_routes import document_routes
from app.routes.query_routes import query_routes

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(document_routes, url_prefix='/documents')
app.register_blueprint(query_routes, url_prefix='/query')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # Default to 6000
    app.run(host='0.0.0.0', port=port, debug=True)
