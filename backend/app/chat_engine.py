from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import pipeline, AutoTokenizer
from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore")

load_dotenv()

# Use the same embedding model that was used to create the vector store
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load existing vector store
vector_store = Chroma(
    persist_directory="data/vectorstore/rti",
    embedding_function=embedding_model
)

retriever = vector_store.as_retriever(search_kwargs={"k": 2})

# Initialize a lightweight text generation model
try:
    # Use a small, efficient model for text generation
    text_generator = pipeline(
        "text2text-generation",
        model="google/flan-t5-small",
        tokenizer="google/flan-t5-small",
        max_length=300,
        do_sample=True,
        temperature=0.7
    )
    # Get tokenizer for length checking
    tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
    llm_available = True
except Exception as e:
    print(f"LLM not available: {e}")
    text_generator = None
    tokenizer = None
    llm_available = False

def get_response(query: str) -> str:
    try:
        # Get relevant documents
        docs = retriever.get_relevant_documents(query)
        
        if not docs:
            return "I couldn't find relevant information about your query in the RTI Act."
        
        # Combine context from relevant documents
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # Use fallback response for now due to token length issues with flan-t5-small
        # The model has a 512 token limit which is too restrictive for legal documents
        return format_fallback_response(context, query)
            
    except Exception as e:
        return f"Error processing query: {str(e)}"

def format_fallback_response(context: str, query: str) -> str:
    """Format a response when LLM is not available"""
    import re
    
    # Advanced text cleaning for corrupted documents
    text = context
    
    # Remove obvious encoding artifacts and repeated patterns
    text = re.sub(r'[^\w\s\.\,\:\;\-\(\)\[\]\'\"]+', ' ', text)
    text = re.sub(r'\b\w{1,2}\b', ' ', text)  # Remove 1-2 character words (likely artifacts)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'(\b\w+\b)(\s+\1\b){2,}', r'\1', text)  # Remove repeated words
    
    # Extract meaningful phrases (at least 4 words, contains "Act" or "information" or "right")
    sentences = re.split(r'[\.!?]+', text)
    good_sentences = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        word_count = len(sentence.split())
        if (word_count >= 4 and 
            any(keyword in sentence.lower() for keyword in ['act', 'information', 'right', 'section', 'authority']) and
            not any(bad in sentence.lower() for bad in ['government of india ministry', 'modified up to'])):
            good_sentences.append(sentence)
    
    if good_sentences:
        # Take best sentences (limit to avoid repetition)
        unique_sentences = []
        for sentence in good_sentences[:5]:
            if not any(sentence.lower() in existing.lower() or existing.lower() in sentence.lower() 
                      for existing in unique_sentences):
                unique_sentences.append(sentence)
        
        result = '. '.join(unique_sentences[:3])
        if result.strip():
            return f"Based on the RTI Act:\n\n{result}.\n\n[Source: RTI Act document sections]"
    
    # If no good content extracted, return a minimal response
    return "I found information about the RTI Act in the documents, but the text appears to be corrupted. Please try rephrasing your question or check if the document source needs to be updated.\n\n[Source: RTI Act document sections]"
