import streamlit as strl
import os
from dotenv import load_dotenv

# App layout configurations
strl.set_page_config(page_title="Financial News RAG Tool", layout="wide", page_icon="📈")

load_dotenv()

from loaders.url_loader import FinancialURLLoader
from embeddings.vector_store import VectorStoreManager
from retrieval.rag_engine import RAGEngine
from utils.pdf_generator import generate_pdf_report

# Initialize Engine Components
v_manager = VectorStoreManager()
rag_engine = RAGEngine()

# Session State Architecture Init
if "vector_store" not in strl.session_state:
    strl.session_state.vector_store = v_manager.load_local_index()
if "summary" not in strl.session_state:
    strl.session_state.summary = None
if "chat_history" not in strl.session_state:
    strl.session_state.chat_history = []
if "processed_urls" not in strl.session_state:
    strl.session_state.processed_urls = []

# Header UI Element
strl.title("📈 Modular Financial News Research Tool")
strl.markdown("An institutional-grade application using **Retrieval-Augmented Generation (RAG)** to parse market data, evaluate sentiments, and trace references precisely.")

# Sidebar Controls
strl.sidebar.header("📋 Target URL Pipeline")
strl.sidebar.write("Input up to 10 financial news article links below:")

url_inputs = []
for i in range(10):
    url = strl.sidebar.text_input(f"URL {i+1}", key=f"url_in_{i}")
    url_inputs.append(url)

process_clicked = strl.sidebar.button("⚙️ Ingest & Process Articles", type="primary")

# API Guardrail Validation Check
# API Guardrail Validation Check
if not os.getenv("GOOGLE_API_KEY"):
    strl.error("⚠️ CRITICAL ERROR: Environment variable `GOOGLE_API_KEY` is missing. Please create a `.env` file.")

# core Data Ingestion Pipeline Execution Flow
if process_clicked:
    active_urls = [u for u in url_inputs if u.strip()]
    if not active_urls:
        strl.sidebar.warning("Please enter at least one valid article URL link.")
    else:
        with strl.spinner("Scraping Web Targets & Sanitizing Text Corpus..."):
            loader = FinancialURLLoader(active_urls)
            documents = loader.load()
            
            if not documents:
                strl.error("Extraction Failed: Could not gather meaningful textual records from specified URLs.")
            else:
                strl.info(f"Loaded {len(documents)} distinct legal/financial document nodes successfully.")
                
                with strl.spinner("Generating High-Dimensional Vector Embeddings & Building Index..."):
                    vs = v_manager.process_and_save(documents)
                    strl.session_state.vector_store = vs
                    strl.session_state.processed_urls = active_urls
                    
                with strl.spinner("Executing MapReduce Synthesis Chains & Aggregating Sentiments..."):
                    summary = rag_engine.generate_global_summary(documents)
                    strl.session_state.summary = summary
                strl.success("Processing Pipeline Complete! Data is safely vectorized locally.")

# Main Layout Window Segmentation Split
col_left, col_right = strl.columns([1, 1])

with col_left:
    strl.header("📋 Unified Corporate Synthesis Briefing")
    if strl.session_state.summary:
        strl.markdown(strl.session_state.summary)
        
        # Download Controls
        pdf_bytes = generate_pdf_report(strl.session_state.summary, strl.session_state.chat_history)
        strl.download_button(
            label="📥 Download Research Report Package (PDF)",
            data=bytes(pdf_bytes),
            file_name="Financial_Equity_Research_Report.pdf",
            mime="application/pdf"
        )
    else:
        strl.info("Input valid target paths via the pipeline drawer layout to render analytics summary profiles here.")

with col_right:
    strl.header("🔍 Grounded RAG Query Panel")
    
    if strl.session_state.vector_store is None:
        strl.warning("Vector Indexing Cache is offline. Provide operational target URLs to enable deep analytical querying features.")
    else:
        # Chat interface panel wrapper
        query = strl.text_input("Pose quantitative/strategic questions directly to the underlying source articles:", placeholder="e.g., What are the primary revenue roadblocks mentioned?")
        
        if strl.button("Query Knowledge Base", type="secondary"):
            if query.strip():
                with strl.spinner("Scanning high-dimensional workspace & cross-examining context chunks..."):
                    result = rag_engine.answer_question(query, strl.session_state.vector_store)
                    
                    # Log to state memory 
                    strl.session_state.chat_history.append({
                        "question": query,
                        "answer": result["answer"]
                    })
                    
                    # Display response
                    strl.markdown("### 📊 Analyst Response")
                    strl.write(result["answer"])
                    
                    # Display Sources and Citations
                    strl.markdown("### 🔗 Verifiable Source Attribution")
                    for src in result["sources"]:
                        strl.markdown(f"- **[Source {src['id']}]** [{src['title']}]({src['url']})")
            else:
                strl.warning("Please supply an explicit query expression.")
                
        # History Dropdowns
        if strl.session_state.chat_history:
            with strl.expander("👁️ Review Active Query Stream Log"):
                for entry in reversed(strl.session_state.session_state.get('chat_history', [])):
                    strl.markdown(f"**Q:** {entry['question']}")
                    strl.markdown(f"**A:** {entry['answer']}")
                    strl.markdown("---")