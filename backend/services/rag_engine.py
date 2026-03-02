import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from chromadb.config import Settings

DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')
CHROMA_DIR = os.path.join(os.path.dirname(__file__), '../data/chroma')

class RAGEngine:
    def __init__(self):
        self.vectorstore = None
        self._load_documents()

    def _load_documents(self):
        pdf_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.pdf')]
        docs = []
        for pdf in pdf_files:
            loader = PyPDFLoader(os.path.join(DATA_DIR, pdf))
            docs.extend(loader.load())
        if docs:
            self.vectorstore = Chroma.from_documents(
                docs,
                OpenAIEmbeddings(),
                persist_directory=CHROMA_DIR,
                client_settings=Settings(anonymized_telemetry=False)
            )

    def query(self, question: str):
        if not self.vectorstore:
            return {
                "answer": "I don't have verified information on that in my current records.",
                "sources": [],
                "risk_level": "Low"
            }
        chain = RetrievalQA.from_chain_type(
            llm=None,  # Replace with your LLM instance
            retriever=self.vectorstore.as_retriever(),
            return_source_documents=True
        )
        result = chain({"query": question})
        sources = [doc.metadata.get('source', '') for doc in result.get('source_documents', [])]
        return {
            "answer": result.get('result', "I don't have verified information on that in my current records."),
            "sources": sources,
            "risk_level": "Low"
        }
