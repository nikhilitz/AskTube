import os
import shutil
from typing import List
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# ✅ Reusable embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def save_to_faiss(docs: List[Document], path: str = "data/faiss_index"):
    """
    Embeds documents and saves them to FAISS vector store.
    If index already exists at path, it is overwritten.
    """
    # Clean previous FAISS index
    if os.path.exists(path):
        shutil.rmtree(path)

    vectorstore = FAISS.from_documents(docs, embedding_model)
    vectorstore.save_local(folder_path=path)
    print(f"[✅] FAISS index saved at: {path}")


def load_faiss_index(path: str = "data/faiss_index", model=None) -> FAISS:
    """
    Loads FAISS vector store from disk using the same embedding model.
    """
    model = model or embedding_model
    return FAISS.load_local(
        folder_path=path,
        embeddings=model,
        allow_dangerous_deserialization=True  # Needed for loading saved index
    )


def similarity_search(query: str, vectorstore: FAISS, k: int = 3) -> List[Document]:
    """
    Perform similarity search on the provided FAISS vectorstore.
    """
    return vectorstore.similarity_search(query, k=k)
