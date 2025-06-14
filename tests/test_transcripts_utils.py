import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.transcript_utils import get_transcript, clean_transcript

def test_transcript_fetching():
    url = "https://www.youtube.com/watch?v=lezL2JpYCM8"
    print("[INFO] Fetching transcript...")
    raw_transcript = get_transcript(url)
    print(f"[INFO] Number of segments: {len(raw_transcript)}")
    cleaned_text = clean_transcript(raw_transcript)
    print(f"[INFO] Cleaned transcript (first 500 chars):\n{cleaned_text[:500]}...")

if __name__ == "__main__":
    test_transcript_fetching()

