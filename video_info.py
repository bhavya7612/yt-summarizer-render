import os
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptAvailable, NoTranscriptFound
from dotenv import load_dotenv
load_dotenv()

# fetch transcript through youtube-transcript-api
def get_video_transcript(video_id):                                                # method-1
    proxies={
        "http":f"{os.getenv('proxy1')}"
    }

    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, proxies={'https':'http://localhost:8080'})
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