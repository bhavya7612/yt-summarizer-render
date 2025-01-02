import os
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptAvailable, NoTranscriptFound
from dotenv import load_dotenv
load_dotenv()

yt_api_key=os.getenv("YT_API_KEY")
youtube = build('youtube', 'v3', developerKey=yt_api_key)

# get video info through api_key
def get_video_title(video_id):
    try:
        request=youtube.videos().list(part="snippet", id=video_id)
        response=request.execute()
        video_title=response['items'][0]['snippet']['title']
        return video_title
    except Exception as e:
        print(f"error is {e}")

# fetch transcript through youtube-transcript-api
def get_video_transcript(video_id):                                                # method-1
    proxies={
        "http":f"{os.getenv('proxy1')}"
    }

    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, proxies=proxies)
        transcript_text = ' '.join([d['text'] for d in transcript_list])
        return transcript_text
    
    except TranscriptsDisabled as e:
        print(f"Error is {e}")
        
    except NoTranscriptAvailable as e:
        print(f"Error is {e}")
    
    except NoTranscriptFound as e:
        print(f"Error is {e}")


if __name__ == '__main__':
    video_id='lzILoMjEpaE'
    transcript=get_video_transcript(video_id)
    print(transcript)