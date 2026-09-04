from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document


def load_document(file_path: Path) -> List[Document]:
    suffix = file_path.suffix.lower()
    if suffix == ".pdf":
        loader = PyPDFLoader(str(file_path))
        return loader.load()
    if suffix in {".txt", ".md", ".markdown"}:
        loader = TextLoader(str(file_path), encoding="utf-8")
        return loader.load()
    raise ValueError(f"Unsupported file type: {suffix}")


def load_directory(directory: Path) -> List[Document]:
    documents: List[Document] = []
    if not directory.exists():
        return documents
    for path in directory.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".pdf", ".txt", ".md", ".markdown"}:
            try:
                documents.extend(load_document(path))
            except Exception:
                continue
    return documents
