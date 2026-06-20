# Financial-news-research-tool

> Streamlit-based RAG tool for financial news analysis and report generation.

![GitHub stars](https://img.shields.io/github/stars/sanjiv-123-su/Financial-news-research-tool?style=for-the-badge&logo=github) ![GitHub forks](https://img.shields.io/github/forks/sanjiv-123-su/Financial-news-research-tool?style=for-the-badge&logo=github) ![GitHub issues](https://img.shields.io/github/issues/sanjiv-123-su/Financial-news-research-tool?style=for-the-badge&logo=github) ![Last commit](https://img.shields.io/github/last-commit/sanjiv-123-su/Financial-news-research-tool?style=for-the-badge&logo=github) ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## 📑 Table of Contents

- [Description](#description)
- [Key Features](#key-features)
- [Use Cases](#use-cases)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Key Dependencies](#key-dependencies)
- [Project Structure](#project-structure)
- [Development Setup](#development-setup)
- [Contributing](#contributing)

## 📝 Description

Financial-news-research-tool is an interactive web-based utility designed to ingest, analyze, and query financial news from external URLs. Built on top of Streamlit, the tool provides an accessible interface for users to perform Retrieval-Augmented Generation (RAG) over financial articles, helping researchers and analysts extract insights without manual search.

## ✨ Key Features

- **🌐 Financial URL Document Ingestion** — Utilizes a specialized URL loader to parse and import content from online financial news sources directly into the application.
- **🗄️ Local Vector Store Management** — Leverages a vector store manager to build, index, and load local embeddings for rapid semantic document retrieval.
- **🤖 Contextual Retrieval-Augmented Generation** — Implements an interactive RAG engine with conversational session tracking to answer complex queries based on source material.
- **📄 Automated PDF Report Generation** — Compiles summarized insights and research results into clean, downloadable PDF files using an integrated utility module.
- **📈 Interactive Streamlit Dashboard** — Provides a clean, wide-layout user interface equipped with session-state architecture to track chat history and current summaries.

## 🎯 Use Cases

- Conducting conversational Q&A research over loaded financial web articles.
- Generating downloadable PDF summaries of market developments for sharing with stakeholders.
- Indexing and querying historical financial updates stored in local vector embeddings.

## 🛠️ Tech Stack

- 🐍 **Python**

**Notable libraries:** LangChain

## ⚡ Quick Start

```bash

# 1. Clone the repository
git clone https://github.com/sanjiv-123-su/Financial-news-research-tool.git

# 2. Create & activate a virtualenv
python -m venv venv && source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

## 📦 Key Dependencies

```
streamlit: 1.35.0
langchain: 0.2.1
langchain-openai: 0.1.8
langchain-google-genai: 1.0.6
langchain-community: 0.2.1
faiss-cpu: 1.8.0
beautifulsoup4: 4.12.3
requests: 2.32.3
fpdf2: 2.7.8
python-dotenv: 1.0.1
```

## 📁 Project Structure

```
.
├── app.py
├── data
│   └── faiss_index
│       ├── index.faiss
│       └── index.pkl
├── embeddings
│   └── vector_store.py
├── loaders
│   └── url_loader.py
├── prompts
│   └── templates.py
├── requirements.txt
├── retrieval
│   └── rag_engine.py
└── utils
    └── pdf_generator.py
```

## 🛠️ Development Setup

### Python
1. Install Python (v3.10+ recommended)
2. `python -m venv venv && source venv/bin/activate`  (Windows: `venv\Scripts\activate`)
3. `pip install -r requirements.txt`

## 👥 Contributing

Contributions are welcome! Here's the standard flow:

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/sanjiv-123-su/Financial-news-research-tool.git`
3. **Branch**: `git checkout -b feature/your-feature`
4. **Commit**: `git commit -m 'feat: add some feature'`
5. **Push**: `git push origin feature/your-feature`
6. **Open** a pull request



