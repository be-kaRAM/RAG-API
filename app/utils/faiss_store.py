# import faiss
# import numpy as np
# import pickle
# import os

# class FaissStore:
#     def __init__(self, dimension):
#         self.index = faiss.IndexFlatL2(dimension)
#         self.document_map = {}  # Maps vector IDs to document metadata
#         self.dimension = dimension
#         self._load_if_exists()
#         print(f"Store initialized with {self.index.ntotal} vectors")

#     def _load_if_exists(self):
#         if os.path.exists('faiss_store.pkl'):
#             with open('faiss_store.pkl', 'rb') as f:
#                 saved = pickle.load(f)
#                 self.index = saved.index
#                 self.document_map = saved.document_map
#             print("Loaded existing store")

#     def save(self):
#         with open('faiss_store.pkl', 'wb') as f:
#             pickle.dump(self, f)
#         print(f"Saved store with {self.index.ntotal} vectors")

#     def add(self, vector, metadata):
#         if len(vector) != self.dimension:
#             raise ValueError(f"Vector must be of dimension {self.dimension}")
#         self.index.add(np.array([vector], dtype=np.float32))
#         vector_id = self.index.ntotal - 1
#         self.document_map[vector_id] = metadata

#     def search(self, query_vector, top_k=3):
#         if len(query_vector) != self.dimension:
#             raise ValueError(f"Query vector must be of dimension {self.dimension}")
#         distances, indices = self.index.search(np.array([query_vector], dtype=np.float32), top_k)
#         results = [self.document_map[idx] for idx in indices[0] if idx != -1]
#         return results
    
#     def clear(self):
#         self.index = faiss.IndexFlatL2(self.dimension)  # Reinitialize the FAISS index
#         self.document_map.clear()  # Clear the metadata map
#         print("All vectors and metadata have been cleared.")


# store = FaissStore(1024)
import faiss
import numpy as np
import pickle
import os

class FaissStore:
    def __init__(self, dimension):
        self.index = faiss.IndexFlatL2(dimension)
        self.document_map = {}  # Maps vector IDs to document metadata
        self.dimension = dimension
        self._load_if_exists()
        print(f"Store initialized with {self.index.ntotal} vectors")

    def _load_if_exists(self):
        """Load the FAISS store if the file exists and is valid."""
        if os.path.exists('faiss_store.pkl'):
            try:
                with open('faiss_store.pkl', 'rb') as f:
                    saved = pickle.load(f)
                    self.index = saved.index
                    self.document_map = saved.document_map
                print("Loaded existing store")
            except (EOFError, pickle.UnpicklingError):
                print("Failed to load store: File is empty or corrupted. Initializing new store.")
                self.index = faiss.IndexFlatL2(self.dimension)
                self.document_map = {}

    def save(self):
        """Save the FAISS store to a file."""
        temp_file = 'faiss_store_temp.pkl'
        try:
            with open(temp_file, 'wb') as f:
                pickle.dump(self, f)
            os.rename(temp_file, 'faiss_store.pkl')  # Replace the file atomically
            print(f"Saved store with {self.index.ntotal} vectors")
        except Exception as e:
            print(f"Error saving store: {e}")

    def add(self, vector, metadata):
        """Add a vector and its metadata to the store."""
        if len(vector) != self.dimension:
            raise ValueError(f"Vector must be of dimension {self.dimension}")
        self.index.add(np.array([vector], dtype=np.float32))
        vector_id = self.index.ntotal - 1
        self.document_map[vector_id] = metadata

    def search(self, query_vector, top_k=3):
        """Search for the top K nearest neighbors of the query vector."""
        if len(query_vector) != self.dimension:
            raise ValueError(f"Query vector must be of dimension {self.dimension}")
        distances, indices = self.index.search(np.array([query_vector], dtype=np.float32), top_k)
        results = [
            self.document_map[idx]
            for idx in indices[0]
            if idx != -1 and idx in self.document_map
        ]
        return results

    def clear(self):
        """Clear all vectors and metadata from the store."""
        self.index = faiss.IndexFlatL2(self.dimension)  # Reinitialize the FAISS index
        self.document_map.clear()  # Clear the metadata map
        print("All vectors and metadata have been cleared.")

# Initialize the FAISS store
store = FaissStore(1024)
