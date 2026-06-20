from langchain_google_genai import ChatGoogleGenerativeAI
from prompts.templates import QA_PROMPT, SUMMARY_PROMPT

class RAGEngine:
    def __init__(self):
        # Operational LLM for text synthesis
        # ✅ Current stable model
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    def answer_question(self, query: str, vector_store) -> dict:
        # CONFIGURE: Tell the retriever to look for a matching text block structure
        retriever = vector_store.as_retriever(
            search_kwargs={
                "k": 5
            }
        )
        relevant_docs = retriever.invoke(query)
        
        if not relevant_docs:
            return {"answer": "No relevant context found to answer the question.", "sources": []}
        
        context_str = ""
        sources = []
        for doc in relevant_docs:
            src_idx = doc.metadata.get("source_id", "?")
            context_str += f"[Source {src_idx}] (Title: {doc.metadata.get('title')}): {doc.page_content}\n\n"
            
            source_info = {
                "id": src_idx,
                "title": doc.metadata.get("title"),
                "url": doc.metadata.get("source")
            }
            if source_info not in sources:
                sources.append(source_info)

        formatted_prompt = QA_PROMPT.format(context=context_str, question=query)
        response = self.llm.invoke(formatted_prompt)
        
        return {
            "answer": response.content,
            "sources": sources,
            "raw_chunks": relevant_docs
        }

    def generate_global_summary(self, documents) -> str:
        if not documents:
            return "No valid document content loaded to summarize."
        
        summaries = []
        for doc in documents:
            prompt = SUMMARY_PROMPT.format(text=doc.page_content)
            res = self.llm.invoke(prompt)
            summaries.append(res.content)
            
        if len(summaries) == 1:
            return summaries[0]
            
        combined_summaries = "\n\n--- Next Article Summary ---\n\n".join(summaries)
        master_prompt = f"""You are a Chief Investment Officer. Synthesize the following individual article briefs into one cohesive Master Equity Research Briefing containing an Executive Summary, Global Key Insights, Aggregated Threats/Risks, Market Opportunities, and a combined Market Sentiment statement with an average Confidence Score.

        {combined_summaries}
        """
        master_response = self.llm.invoke(master_prompt)
        return master_response.content