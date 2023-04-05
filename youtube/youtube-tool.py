from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

def extract_transcript(video_id):
    res = YouTubeTranscriptApi.get_transcript(video_id)
    # map over res and extraxt text then join all texts together in a single string seperated by \n code:
    youtube_transcript = "\n".join([ f"{r['start']}: {r['text']}" for r in res])
    return youtube_transcript

def summarize_video_transcript(video_id):
    youtube_transcript = extract_transcript(video_id)
    # keep only the first 100 characters of the summary
    youtube_transcript = youtube_transcript[:1000]

    summarizer = pipeline("summarization")
    summary = summarizer(youtube_transcript, max_length=100, min_length=30, do_sample=False)
    return summary

if __name__ == '__main__':
    formatted_transcript_text = extract_transcript('ntz160EnWIc')
    video_summary = summarize_video_transcript('ntz160EnWIc')
    print()