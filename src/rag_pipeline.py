import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from google import genai
import chromadb

class LocalRAGPipeline:
    def __init__(self, db_dir="./chroma_db"):
        self.client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))
        self.chroma_client = chromadb.PersistentClient(path=db_dir)
        self.collection = self.chroma_client.get_or_create_collection(name="support_kb")

    def get_embedding(self, text: str) -> list:
        """Helper to call Gemini Embedding models."""
        response = self.client.models.embed_content(
            model="gemini-embedding-2",
            contents=text
        )
        return response.embeddings[0].values

    def ingest_document(self, doc_name: str, content: str):
        """Split document and add the chunks to the vector database."""
        splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=40)
        chunks = splitter.split_text(content)
        for idx, chunk in enumerate(chunks):
            embedding = self.get_embedding(chunk)
            chunk_id = f"{doc_name}_chunk_{idx}"
            self.collection.add(
                ids=[chunk_id],
                embeddings=[embedding],
                metadatas=[{"source": doc_name, "chunk_index": idx}],
                documents=[chunk]
            )

    def retrieve_context(self, query: str, top_k: int = 2) -> list:
        """Perform search based on cosine similarity scores."""
        query_vector = self.get_embedding(query)
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=top_k
        )
        
        # Format clean lists of context outputs for prompt insertion
        retrieved_items = []
        if results and results.get('documents'):
            for i in range(len(results['documents'][0])):
                retrieved_items.append({
                    "text": results['documents'][0][i],
                    "source": results['metadatas'][0][i]['source'],
                    # Chroma returns distance metrics, translate to a simulated confidence score
                    "score": 1.0 - (results['distances'][0][i] if results.get('distances') else 0.0)
                })
        return retrieved_items