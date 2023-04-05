from youtube_transcript_api import YouTubeTranscriptApi


if __name__ == '__main__':
    res = YouTubeTranscriptApi.get_transcript('ntz160EnWIc')
    res
    # map over res and extraxt text then join all texts together in a single string seperated by \n code:
    youtube_transcript = "\n".join([r['text'] for r in res])
    youtube_transcript