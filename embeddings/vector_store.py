import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

DB_FAISS_PATH = os.path.join("data", "faiss_index")

class VectorStoreManager:
    def __init__(self):
        # FIX: Re-insert "models/" and explicitly specify the task type to pass Google's Batch API validation
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            api_version="v1"          # forces v1 endpoint, not v1beta
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )

    def process_and_save(self, documents):
        if not documents:
            return None
        chunks = self.text_splitter.split_documents(documents)
        vector_store = FAISS.from_documents(chunks, self.embeddings)
        os.makedirs("data", exist_ok=True)
        vector_store.save_local(DB_FAISS_PATH)
        return vector_store

    def load_local_index(self):
        if os.path.exists(DB_FAISS_PATH):
            return FAISS.load_local(DB_FAISS_PATH, self.embeddings, allow_dangerous_deserialization=True)
        return None