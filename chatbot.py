import os
import hashlib
import re
import base64
import streamlit as st
from PyPDF2 import PdfReader
from PIL import Image
from sentence_transformers import SentenceTransformer
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import Ollama
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.schema import Document

# ------------------------------
# Configuration
# ------------------------------
os.environ["STREAMLIT_SERVER_ENABLE_FILE_WATCHER"] = "false"

# Load Embedding Model
embed_model = SentenceTransformer("all-mpnet-base-v2")

# Configuration
os.environ["STREAMLIT_SERVER_ENABLE_FILE_WATCHER"] = "false"
embed_model = SentenceTransformer("all-mpnet-base-v2")

# Custom CSS for dark sidebar
def set_dark_sidebar():
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background: linear-gradient(135deg, #2b5876 0%, #4e4376 100%) !important;
            color: white !important;
        }
        .sidebar .sidebar-content {
            background-color: #1a1a1a;
        }
        [data-testid="stFileUploader"] {
            color: white !important;
        }
        .st-bq {
            border-color: white;
        }
        .st-c7 {
            background-color: rgba(255,255,255,0.1);
        }
    </style>
    """, unsafe_allow_html=True)

# Text Processing Functions
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\[\d+\]', '', text)
    return text.strip()

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page_num, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += f"--- PAGE {page_num+1} ---\n{clean_text(page_text)}\n\n"
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len
    )
    return text_splitter.split_text(text)

# Vector Store Functions
def get_vector_store(text_chunks):
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(
        name="pdf_reader",
        metadata={"hnsw:space": "cosine"}
    )
    
    for i, chunk in enumerate(text_chunks):
        chunk_id = f"chunk_{i}_{hashlib.md5(chunk.encode()).hexdigest()}"
        collection.add(
            ids=[chunk_id],
            documents=[chunk],
            embeddings=[embed_model.encode(chunk, normalize_embeddings=True).tolist()],
            metadatas=[{"chunk_num": i, "type": "text_chunk"}]
        )

# Optimized QA Chain
def get_conversational_chain():
    """Create optimized QA chain with finely-tuned prompt"""
    prompt_template = """
    **Document Analysis Task**
    
    You are a senior research assistant analyzing documents. Follow these guidelines precisely:

    ### Context:
    {context}

    ### Question:
    {question}

    ### Response Requirements:
    1. **Accuracy**:
       - Answer must be directly extractable from context
       - No extrapolation or personal knowledge
       - If unsure: "The documents do not contain this information"

    2. **Format**:
       - First sentence: Direct answer
       - Subsequent sentences: Supporting evidence
       - End with: (Source: Chunk [X])

    3. **Precision**:
       - Use exact figures/dates when available
       - For comparisons: Use "more than"/"less than" rather than exact percentages
       - Technical terms: Keep verbatim from text

    4. **Length**:
       - Simple facts: 1 sentence
       - Complex answers: 3 sentences max
       - Lists: Max 3 items with "..." if truncated

    ### Examples:
    Good: "The project budget is $1.2 million (Source: Chunk 2)"
    Bad: "I think it's around a million dollars"

    Good: "Three main risks were identified: 1) Market volatility 2) Supply chain... (Source: Chunks 3,5)"
    Bad: "There are several risks"

    ### Your Analysis:
    1. First verify question is answerable from context
    2. Identify all relevant context sections
    3. Extract verbatim evidence
    4. Compose response following requirements

    ### Final Answer:
    """
    
    model = Ollama(
        model="mistral",
        temperature=0.2,  # Lower for more factual responses
        top_k=30,
        top_p=0.85
    )
    
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    
    return load_qa_chain(
        model,
        chain_type="stuff",
        prompt=prompt,
        verbose=False
    )
# Query Processing
def user_input(user_question):
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection("pdf_reader")
    
    results = collection.query(
        query_embeddings=[embed_model.encode(user_question, normalize_embeddings=True).tolist()],
        n_results=3,
        include=["documents", "metadatas"]
    )
    
    relevant_docs = [
        Document(page_content=doc, metadata=meta)
        for doc, meta in zip(results['documents'][0], results['metadatas'][0])
    ]
    
    if relevant_docs:
        response = get_conversational_chain()(
            {"input_documents": relevant_docs, "question": user_question},
            return_only_outputs=True
        )
        st.markdown(f"**Answer:** {response['output_text']}")
    else:
        st.warning("No relevant information found")

# Streamlit UI
def main():
    st.set_page_config("PDF Analyzer", page_icon="🤖", layout="wide")

    # Set dark sidebar theme
    set_dark_sidebar()
    
    # Document Upload Section
    with st.sidebar:
        # Chatbot image at top
        st.image("Img/bot.jpg")
        st.markdown("<h1 style='text-align: center; color: white;'>PDF Analyzer</h1>", unsafe_allow_html=True)
        
        st.subheader("📁 Document Upload")
        pdf_docs = st.file_uploader(
            "Choose PDF files", 
            type="pdf",
            accept_multiple_files=True,
            label_visibility="collapsed"
        )
        
        if st.button("⚡ Process Documents", type="primary"):
            if not pdf_docs:
                st.warning("Please upload files first")
            else:
                with st.spinner("Processing documents..."):
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    get_vector_store(text_chunks)
                st.success("✅ Documents processed successfully!")
        # Developer info at bottom
        st.markdown("""
        <div style="position: fixed; bottom: 20px; width: 100%; text-align: center;">
            <p style="color: white;">Developed by</p>
            <h4 style="color: #4FC3F7;">Developed by Kameshwaran</h4>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.title("Document Analysis Assistant")
        st.markdown("---")
        
        user_question = st.text_input(
            "Ask a question about your documents:",
            placeholder="Type your question here...",
            key="query"
        )
        
        if user_question:
            user_input(user_question)
    
    with col2:
        # Optional: Add additional visual elements
        st.markdown("### Quick Tips")
        st.info("""
        - Upload multiple PDFs
        - Ask specific questions
        - Get cited answers
        """)

if __name__ == "__main__":
    main()