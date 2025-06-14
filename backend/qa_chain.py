from dotenv import load_dotenv
import os
import sys

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ✅ Add root path for backend imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.vector_store import load_faiss_index, similarity_search

# ✅ Load environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
api_base = os.getenv("OPENAI_API_BASE")

if not api_key or not api_base:
    raise ValueError("❌ OPENAI_API_KEY or OPENAI_API_BASE is missing from your .env file")

# ✅ Initialize OpenAI-compatible LangChain LLM
llm = ChatOpenAI(
    model_name="provider-2/gpt-3.5-turbo",  # Or "openai/gpt-4o"
    temperature=0.7,
)

# ✅ Prompt template for RAG
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful assistant. Use the following transcript context to answer the question.

Context:
{context}

Question:
{question}

Answer in a clear and concise way.
""",
)

# ✅ Build QA chain (loads latest vectorstore each time)
def build_qa_chain(vectorstore=None):
    # Lazy load if not passed
    if vectorstore is None:
        vectorstore = load_faiss_index("data/faiss_index")

    return (
        # Step 1: Retrieve context
        (lambda q: {
            "context": "\n".join(
                [doc.page_content for doc in similarity_search(q, vectorstore)]
            ),
            "question": q,
        })
        # Step 2: Format the prompt
        | prompt
        # Step 3: Run LLM
        | llm
        # Step 4: Parse output
        | StrOutputParser()
    )

# ✅ CLI test
if __name__ == "__main__":
    chain = build_qa_chain()
    query = input("AskTube ❓ Enter your question: ")
    answer = chain.invoke(query)
    print("\n📢 Answer:\n", answer)
