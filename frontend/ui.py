import streamlit as st
from langchain.schema import Document
import sys
import os

# ✅ Allow backend imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.transcript_utils import get_transcript, clean_transcript
from backend.text_splitter import split_transcript
from backend.vector_store import save_to_faiss, load_faiss_index
from backend.qa_chain import build_qa_chain

# 🎥 App Title
st.title("🎥 AskTube - Chat with YouTube Videos")

# 📥 Step 1: Get video URL
url = st.text_input("Enter YouTube video URL")

if st.button("Index Video"):
    with st.spinner("📡 Fetching and indexing transcript..."):
        try:
            raw = get_transcript(url)
            if not raw:
                st.warning("⚠️ No transcript found. Try another video.")
            else:
                cleaned = clean_transcript(raw)
                chunks = split_transcript(cleaned)
                if len(chunks) == 0:
                    st.warning("⚠️ Transcript is too short to index.")
                else:
                    documents = [Document(page_content=chunk) for chunk in chunks]
                    save_to_faiss(documents)  # saves to `data/faiss_index`
                    st.success("✅ Video indexed successfully!")
        except Exception as e:
            st.error(f"❌ Failed to index video: {str(e)}")

# Divider
st.divider()

# ❓ Step 2: Ask a question
question = st.text_input("Ask a question about the video")

if st.button("Get Answer"):
    with st.spinner("🤖 Generating answer..."):
        try:
            # 🔄 Load latest FAISS index
            vectorstore = load_faiss_index("data/faiss_index")
            chain = build_qa_chain(vectorstore=vectorstore)
            answer = chain.invoke(question)
            st.markdown(f"**📢 Answer:** {answer}")
        except Exception as e:
            st.error(f"❌ Failed to get answer: {str(e)}")
