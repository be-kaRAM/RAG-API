from transformers import pipeline
from app.utils.faiss_store import store
import voyageai

DIMENSION = 1024
NUM_CONTEXTS = 1  # Increased to fetch more relevant contexts

# Initialize clients
client = voyageai.Client(api_key="pa-ChDLv8ec57LnZ05xssfSpYZBH6MVEBEjXjqsCZ3ox-0")
qa_pipeline = pipeline(
    "question-answering",
    model="deepset/roberta-base-squad2"
)

def combine_contexts(results):
    """Combine multiple context results intelligently."""
    contexts = [result["text"] for result in results]
    return "\n\n".join(contexts).strip()

def enhance_answer_with_context(answer, context):
    """Expand the answer by finding supporting details in the context."""
    sentences = context.split('.')
    supporting_sentences = [sentence.strip() for sentence in sentences if answer.lower() in sentence.lower()]
    supporting_context = " ".join(supporting_sentences)
    return supporting_context.strip()

def handle_query(query, use_qa_pipeline=True):
    try:
        # Generate query embedding
        embedding_result = client.embed([query], model="voyage-3", input_type="query")
        if not embedding_result or not embedding_result.embeddings:
            return {"error": "Failed to generate embedding for the query."}

        query_embedding = embedding_result.embeddings[0]
        results = store.search(query_embedding, top_k=NUM_CONTEXTS)
        
        if not results:
            return {"error": "No relevant contexts found for the query."}

        context = combine_contexts(results)
        if not context:
            return {"error": "Retrieved context is empty."}

        # Pass inputs directly to pipeline
        result = qa_pipeline(
            question=query,  
            context=context,
            max_answer_len=100  # Allow longer answers
        )

        if not result["answer"].strip():
            return {"error": "No answer generated."}

        # Enhance the answer with additional supporting details
        enhanced_context = enhance_answer_with_context(result["answer"], context)

        return {
            "answer": result["answer"],
            "supporting_context": enhanced_context,
            "full_context": context,
            "confidence": round(float(result["score"]) * 100, 2),
            "sources_used": len(results)
        }

    except Exception as e:
        return {"error": f"Error: {str(e)}"}
