from pathlib import Path
from typing import List, Tuple

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

from src.core.config import get_settings
from src.core.llm import build_chat_model, clear_llm_cache
from src.rag.chunker import chunk_documents
from src.rag.loader import load_document, load_directory
from src.rag.store import get_vector_store


INGEST_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a precise knowledge assistant. Answer only from the provided context. "
            "If the context does not contain the answer, say you do not have that information. "
            "Keep answers concise and suitable for spoken delivery when asked.",
        ),
        (
            "human",
            "Context:\n{context}\n\nQuestion: {question}\n\nAnswer:",
        ),
    ]
)


class AgenticRAGPipeline:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.store = get_vector_store()
        self._llm = None

    @property
    def llm(self):
        if self._llm is None:
            self._llm = build_chat_model(temperature=0.2, max_tokens=512)
        return self._llm

    def reset_llm(self) -> None:
        self._llm = None
        clear_llm_cache()

    def ingest_file(self, file_path: Path) -> int:
        documents = load_document(file_path)
        chunks = chunk_documents(
            documents,
            chunk_size=self.settings.chunk_size,
            chunk_overlap=self.settings.chunk_overlap,
        )
        return self.store.add_documents(chunks)

    def ingest_directory(self, directory: Path | None = None) -> int:
        directory = directory or self.settings.knowledge_path
        documents = load_directory(directory)
        chunks = chunk_documents(
            documents,
            chunk_size=self.settings.chunk_size,
            chunk_overlap=self.settings.chunk_overlap,
        )
        return self.store.add_documents(chunks)

    def retrieve(self, query: str, k: int | None = None) -> List[Document]:
        return self.store.similarity_search(query, k=k)

    def answer(self, question: str, k: int | None = None) -> Tuple[str, List[str]]:
        docs = self.retrieve(question, k=k)
        if not docs:
            return "I do not have that information in the knowledge base.", []
        context = "\n\n".join(doc.page_content for doc in docs)
        sources = [doc.metadata.get("source", "unknown") for doc in docs]
        chain = INGEST_PROMPT | self.llm
        response = chain.invoke({"context": context, "question": question})
        text = response.content if hasattr(response, "content") else str(response)
        return text.strip(), sources


_pipeline: AgenticRAGPipeline | None = None


def get_rag_pipeline() -> AgenticRAGPipeline:
    global _pipeline
    if _pipeline is None:
        _pipeline = AgenticRAGPipeline()
    return _pipeline
