import os
from dotenv import load_dotenv
from src.rag_pipeline import LocalRAGPipeline

# Load the API key
load_dotenv()

def setup_database():
    print("Initializing RAG Pipeline Database...")
    pipeline = LocalRAGPipeline()
    
    data_dir = "./data"
    
    # Loop through every file in your data folder
    for filename in os.listdir(data_dir):
        filepath = os.path.join(data_dir, filename)
        
        # Handle Text and Markdown files
        if filename.endswith(".txt") or filename.endswith(".md"):
            print(f"Reading and chunking {filename}...")
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                pipeline.ingest_document(filename, content)
                
        # Handle PDF files
        elif filename.endswith(".pdf"):
            print(f"Reading and chunking {filename}...")
            from pypdf import PdfReader
            reader = PdfReader(filepath)
            pdf_text = ""
            for page in reader.pages:
                pdf_text += page.extract_text() + "\n"
            pipeline.ingest_document(filename, pdf_text)

    print("\n✅ Database setup complete! Your documents are embedded and ready to be searched.")

if __name__ == "__main__":
    setup_database()