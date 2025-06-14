import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import os
from langchain.schema import Document
from backend.vector_store import save_to_faiss, load_faiss_index, similarity_search

def test_vector_store_pipeline():
    # Create dummy documents
    docs = [
        Document(page_content="Python is a great programming language."),
        Document(page_content="LangChain helps you build LLM apps."),
        Document(page_content="FAISS is used for efficient similarity search."),
    ]

    # Define path
    test_path = "data/test_faiss_index"

    # Clean up before test
    if os.path.exists(test_path):
        import shutil
        shutil.rmtree(test_path)

    # Save to FAISS
    save_to_faiss(docs, path=test_path)

    # Load from FAISS
    loaded_index = load_faiss_index(path=test_path)

    # Run similarity search
    query = "What is LangChain?"
    results = similarity_search(query, loaded_index, k=2)

    # Output results
    print("\n[🔍] Similarity Search Results:")
    for i, doc in enumerate(results):
        print(f"\nResult {i+1}: {doc.page_content}")

    # Assert results
    assert len(results) == 2
    assert any("LangChain" in doc.page_content for doc in results)

if __name__ == "__main__":
    test_vector_store_pipeline()
