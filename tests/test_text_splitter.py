import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.text_splitter import split_transcript
from backend.transcript_utils import get_transcript, clean_transcript

def test_chunking():
    url = "https://www.youtube.com/watch?v=NmblVxyBhi8"
    raw = get_transcript(url)
    print("✅ Raw transcript fetched.")
    cleaned = clean_transcript(raw)
    print("✅ Cleaned transcript length:", len(cleaned))

    chunks = split_transcript(cleaned)
    print(f"✅ Total chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks[:3], 1):
        print(f"\n--- Chunk {i} ---\n{chunk}\n")

if __name__ == "__main__":
    test_chunking()
