from pathlib import Path
from typing import List, Optional

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from src.core.config import get_settings


class VectorStoreService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._embeddings: Optional[HuggingFaceEmbeddings] = None
        self._store: Optional[Chroma] = None

    @property
    def embeddings(self) -> HuggingFaceEmbeddings:
        if self._embeddings is None:
            self._embeddings = HuggingFaceEmbeddings(
                model_name=self.settings.embedding_model,
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True},
            )
        return self._embeddings

    @property
    def store(self) -> Chroma:
        if self._store is None:
            self._store = Chroma(
                collection_name="hr_knowledge",
                embedding_function=self.embeddings,
                persist_directory=str(self.settings.chroma_path),
            )
        return self._store

    def add_documents(self, documents: List[Document]) -> int:
        if not documents:
            return 0
        self.store.add_documents(documents)
        return len(documents)

    def similarity_search(self, query: str, k: Optional[int] = None) -> List[Document]:
        k = k or self.settings.retrieval_k
        return self.store.similarity_search(query, k=k)

    def as_retriever(self, k: Optional[int] = None):
        k = k or self.settings.retrieval_k
        return self.store.as_retriever(search_kwargs={"k": k})


_vector_service: Optional[VectorStoreService] = None


def get_vector_store() -> VectorStoreService:
    global _vector_service
    if _vector_service is None:
        _vector_service = VectorStoreService()
    return _vector_service
