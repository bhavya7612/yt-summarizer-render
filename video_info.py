import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import requests
load_dotenv()

api_key=os.getenv("YT_API_KEY")
creds=Credentials.from_authorized_user_info(
    info={
        "token": os.getenv("token"),
        "refresh_token": os.getenv("refresh_token"),
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": os.getenv("client_id"),
        "client_secret": os.getenv("client_secret"),
        "scopes": ["https://www.googleapis.com/auth/youtube.force-ssl"]
    }
)
youtube = build('youtube', 'v3', developerKey=api_key)

youtube2 = build('youtube', 'v3', credentials=creds)

# get video info through api_key
def get_video_title(video_id):
    try:
        request=youtube.videos().list(part="snippet", id=video_id)
        response=request.execute()
        video_title=response['items'][0]['snippet']['title']
        return video_title
    except Exception as e:
        print(f"error is {e}")

def get_video_transcript(video_id):
    request=youtube2.captions().list(
        part="snippet",
        videoId=video_id
    )
    response=request.execute()

    caption_text=""
    access_token=os.getenv("token")
    for item in response['items']:
        caption_id=item['id']
        url = f"https://www.googleapis.com/youtube/v3/captions/{caption_id}"
        res = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
        if res.status_code == 200:
            caption_text += res.text
        else:
            print(f"Failed to fetch transcript: {res.status_code}, {res.text}")


        # print("Item id:", item['id'])
        # print("Item: ", item)
        # caption_id=item['id']
        # base_url=item['snippet']['baseUrl']
        # file_name=item['snippet']['fileName']

        # caption_url=f"{base_url}/{file_name}"
        # try:
        #     response=requests.get(caption_url)
        #     response.raise_for_status()

        #     caption_text += response.text
        # except requests.exceptions.RequestException as e:
        #     print(f"error downloading caption file: {e}")
    
    return caption_text

# get video info through credentials of OAuth
def list_captions(video_id, youtube2):                        # list captions
    request = youtube2.captions().list(
        part="snippet",
        videoId=video_id
    )
    response = request.execute()
    return response

def download_caption(caption_id, youtube2, video_id):         # download captions
    request = youtube2.captions().download(id=caption_id)
    # Download caption file to disk
    with open(f"{video_id}_captions.srt", "wb") as file:
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download progress: {int(status.progress() * 100)}%")
    
    print(f"Captions downloaded successfully for video {video_id}.")

def get_captions(video_id):                                   # driver function
    response = list_captions(video_id, youtube2)
    
    if response["items"]:
        # Step 2: Get caption ID and download the captions
        caption_id = response["items"][0]["id"]
        print(f"Found caption ID: {caption_id}")
        download_caption(caption_id, youtube2, video_id)
    else:
        print("No captions available for this video.")


# fetch transcript through youtube-transcript-api
def fetch_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        print(f"Error is {e}")
    transcript_text = ' '.join([d['text'] for d in transcript_list])
    return transcript_text

if __name__ == '__main__':
    video_id='fLeJJPxua3E'
    transcript=get_video_transcript(video_id)
    print(transcript)