from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import json
from dotenv import load_dotenv

load_dotenv()


# Load your saved chunks
with open("data/processed_documents/rti_act_chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Initialize embedding model (using free Sentence Transformers)
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Use Chroma for vector storage
vector_store = Chroma.from_texts(
    texts=chunks,
    embedding=embedding_model,
    persist_directory="data/vectorstore/rti"
)

# Chroma now automatically persists data when using persist_directory
print(f"Vector store created successfully! Stored {len(chunks)} chunks in data/vectorstore/rti")
