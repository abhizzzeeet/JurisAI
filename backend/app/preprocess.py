# At the top of preprocess.py
from pathlib import Path
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json

# Define paths based on your project structure
RAW_PDF_PATH = Path("data/raw_documents/RTI-Act_English.pdf")
OUTPUT_JSON_PATH = Path("data/processed_documents/rti_act_chunks.json")


# Step 1: Load PDF
def load_pdf(path):
    reader = PdfReader(path)
    raw_text = ""
    for page in reader.pages:
        raw_text += page.extract_text() or ""
    return raw_text

# Step 2: Chunk the text
def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return splitter.split_text(text)

# Step 3: Save to JSON
def save_chunks(chunks, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

# Run preprocessing
if __name__ == "__main__":
    text = load_pdf(RAW_PDF_PATH)
    chunks = chunk_text(text)
    save_chunks(chunks, OUTPUT_JSON_PATH)
    print(f" Done. {len(chunks)} chunks saved.")
