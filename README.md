# RAG Application

This repository implements a Retrieval-Augmented Generation (RAG) application that processes documents, generates embeddings, stores them in a FAISS vector database, and performs query-based search with context-aware answers.

## Features
- Upload PDF documents and process them into chunks for embedding storage.
- Efficient vector storage and retrieval using FAISS.
- Query system with context-aware answers powered by Transformers.
- REST API endpoints for document upload and query search.
- Dockerized for easy deployment.

## System Design Architecture


1. **Document Processing:**
   - Extracts text from PDFs.
   - Splits content into smaller chunks for embedding generation.
   - Generates embeddings using VoyageAI and stores them in FAISS.

2. **Query Handling:**
   - Embeds the query using VoyageAI.
   - Searches for relevant contexts in FAISS.
   - Answers queries using a question-answering pipeline (Hugging Face Transformers).

3. **Components:**
   - FAISS Vector Store: Efficient storage and retrieval of vector embeddings.
   - REST API: Flask-based endpoints for uploading documents and querying.
   - Dockerized Deployment: Simplifies running the application in different environments.

## File Structure
```plaintext
rag_app/
├── app/
│   ├── __init__.py
│   ├── main.py              # Entry point for FastAPI app
│   ├── routes/              # API route handlers
│   │   ├── __init__.py
│   │   ├── document_routes.py
│   │   ├── query_routes.py
│   ├── services/            # Core logic for processing and querying
│   │   ├── __init__.py
│   │   ├── document_service.py
│   │   ├── query_service.py
│   ├── utils/               # Helper functions or utilities
│   │   ├── __init__.py
│   │   ├── faiss_store.py
│   │   ├── file_handler.py
├── temp/                    # Temporary storage for uploaded files
├── tests/                   # Unit and integration tests
│   ├── __init__.py
│   ├── test_routes.py
├── Dockerfile               # Dockerfile for containerization
├── requirements.txt         # List of dependencies
└── README.md                # Documentation
```

## Setup Instructions

### Local Setup
1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd rag_app
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python -m app.main
   ```

4. **Access the API:**
   - Upload document: `POST /upload`
   - Query search: `POST /search`

### Dockerized Setup
1. **Build the Docker image:**
   ```bash
   docker build -t rag_app .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8000:8000 rag_app
   ```

3. **Access the API:**
   Use `http://localhost:6000` for API endpoints.

## API Documentation

### Upload Document
- **Endpoint:** `POST documents/upload`
- **Description:** Uploads a PDF document and processes it.
- **Request Body:**
  - `file`: PDF file.
- **Response:**
  ```json
  {
    "message": "Document processed and stored successfully"
  }
  ```

### Search Query
- **Endpoint:** `POST query/search`
- **Description:** Searches for answers based on the query.
- **Request Body:**
  ```json
  {
    "query": "Your question here"
  }
  ```
- **Response:**
  ```json
  {
    "answer": "Generated answer",
    "supporting_context": "Relevant context",
    "full_context": "Full document context",
    "confidence": 95.6,
    "sources_used": 1
  }
  ```

## Cost Analysis
### Assumptions
- **Hosting:** AWS EC2 (t2.micro) or similar for 24/7 operation.
- **Embeddings:** VoyageAI usage for embedding generation.
- **Queries:** 1000 queries/day.

| Resource         | Cost Estimate |

| Hosting (24x7)   | $10/month     |
| VoyageAI Usage   | $20/month     |
| Storage (FAISS)  | $5/month      |
| Total            | **$35/month** |

## Known Limitations
- Limited to PDF files for document upload.
- Embedding model and QA pipeline may produce suboptimal results for complex queries.
- Require more tuned query handler , may be paid CHATGPT4

## Potential Improvements
- Add support for other document formats (e.g., Word, text).
- Optimize FAISS for larger-scale applications using disk-based indexing.
- Improve API scalability with additional microservices.
- Extend query capabilities with custom NLP models.

## Sample Queries and Responses
### Query Example
- **Query:** "What is the purpose of FAISS in this application?"
- **Response:**
  ```json
  {
    "answer": "Efficient storage and retrieval of vector embeddings",
    "supporting_context": "FAISS is used to store document embeddings for efficient similarity search.",
    "confidence": 97.2,
    "sources_used": 1
  }
  
