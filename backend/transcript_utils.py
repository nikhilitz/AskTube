from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
from urllib.parse import urlparse, parse_qs
from typing import List, Dict, Union


def extract_video_id(url: str) -> str:
    """
    Extracts the YouTube video ID from a URL.
    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    """
    parsed = urlparse(url)
    if parsed.hostname in ['www.youtube.com', 'youtube.com']:
        return parse_qs(parsed.query).get('v', [None])[0]
    elif parsed.hostname == 'youtu.be':
        return parsed.path[1:] if parsed.path else None
    return None


def get_transcript(video_url: str) -> List[Union[Dict[str, str], object]]:
    """
    Fetches the transcript from a YouTube video.
    Only English transcripts are accepted (manual or auto-generated).

    Returns a list of transcript segments if English is available.
    Raises RuntimeError otherwise.
    """
    video_id = extract_video_id(video_url)
    if not video_id:
        raise ValueError("❌ Invalid YouTube URL: Unable to extract video ID.")

    try:
        # Try direct English transcript fetch (manual or auto-generated)
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        print("✅ English transcript found and fetched.")
        return transcript

    except NoTranscriptFound:
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

            # Check for any transcript with English language code
            for t in transcript_list:
                if t.language_code == 'en':
                    print(f"⚠️ Fallback: Fetched transcript in English ({'auto-generated' if t.is_generated else 'manual'})")
                    return t.fetch()

            raise NoTranscriptFound("No English transcript available.")

        except Exception as e:
            raise RuntimeError(f"❌ English transcript not available: {e}")

    except TranscriptsDisabled:
        raise RuntimeError("❌ Transcripts are disabled for this video.")

    except Exception as e:
        raise RuntimeError(f"❌ Unexpected error while fetching transcript: {e}")


def clean_transcript(transcript: List[Union[Dict[str, str], object]]) -> str:
    """
    Cleans and combines transcript segments into a single plain text string.
    Supports both dict and object segment types from YouTubeTranscriptApi.
    """
    return " ".join(
        segment['text'].strip() if isinstance(segment, dict) else segment.text.strip()
        for segment in transcript
    )
