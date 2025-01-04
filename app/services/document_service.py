import os
from PyPDF2 import PdfReader
from app.utils.faiss_store import FaissStore
import voyageai

# Configuration
TEMP_DIR = "temp/"
DIMENSION = 1024

# Initialize FAISS store and VoyageAI client
store = FaissStore(DIMENSION)
# store.clear()
client = voyageai.Client(api_key="pa-ChDLv8ec57LnZ05xssfSpYZBH6MVEBEjXjqsCZ3ox-0")

def extract_text_from_pdf(filepath):

    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def split_into_chunks(text, chunk_size=500):

    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) <= chunk_size:
            current_chunk += paragraph + "\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = paragraph
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def process_document(file):

    try:
        # Save the uploaded file temporarily
        filepath = os.path.join(TEMP_DIR, file.filename)
        os.makedirs(TEMP_DIR, exist_ok=True)
        file.save(filepath)

        # Extract text from the document
        content = extract_text_from_pdf(filepath)
        if not content or content.strip() == "":
            return {"error": "Failed to extract text from the document"}

        # Split content into smaller chunks
        chunks = split_into_chunks(content)
        print(f"Document split into {len(chunks)} chunks.")

        # Generate embeddings and store them
        for chunk in chunks:
            try:
                # Validate chunk content
                if not chunk.strip():  # Skip empty or whitespace-only chunks
                    print("Skipping empty chunk.")
                    continue

                # Generate embeddings for the chunk
                embedding_result = client.embed([chunk], model="voyage-3", input_type="document")
                print(f"Embedding Result Object: {embedding_result}")

                if not embedding_result or not embedding_result.embeddings:
                    print(f"Failed to generate embedding for chunk: {chunk}")
                    continue  # Skip this chunk

                embedding = embedding_result.embeddings[0]
                # print(f"Embedding Shape: {len(embedding)}")
                # print(f"Embedding Values: {embedding}")  # Print the actual embedding values

                # Validate the embedding size
                if len(embedding) != DIMENSION:
                    print(f"Invalid embedding size. Expected {DIMENSION}, got {len(embedding)}")
                    continue  # Skip invalid embedding

                # Add to FAISS store
                store.add(embedding, {"text": chunk})
                print("Added chunk to FAISS store.")

            except Exception as e:
                print(f"Error processing chunk: {chunk}\nException: {e}")
                continue

        store.save()
        print("Store saved successfully.")

        return {"message": "Document processed and stored successfully"}

    except Exception as e:
        return {"error": f"Processing failed: {str(e)}"}
