from youtube_transcript_api import YouTubeTranscriptApi
import os
import google.generativeai as genai
import translator
from dotenv import load_dotenv
load_dotenv()

def get_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, proxies={"https": "http://192.0.0.4"})
    except Exception as e:
        print(f"Error is {e}")
    transcript_text = ' '.join([d['text'] for d in transcript_list])
    return transcript_text

def abstractive_summarization(transcript_text, lang, max_len):
    api_key=os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    prompt=f"You are Youtube transcript summarizer. Summarize the given transcript text within {max_len} words. The transcript text is:\n{transcript_text} "
    model=genai.GenerativeModel("gemini-1.5-pro")
    try:
        response=model.generate_content(prompt)
        response=translator.translate(response.text, lang)
        return response
    except Exception as e:
        raise e

    # --------------------OR-----------------------

    # summarizer = pipeline('summarization',model='t5-small')
    # summary=''

    # for i in range(0, (len(transcript_text)//500) + 1):
    #     summary_text = summarizer(transcript_text[i * 500:(i+1) * 500], max_length=max_len)[0]['summary_text']
    #     summary = summary + summary_text + ' '
    # return summary

def summarise(video_id, max_len=150, lang="en"):
    try:
        transcript_text = get_transcript(video_id)
    except:
        return "No subtitles available for this video"

    summary = abstractive_summarization(transcript_text, lang, max_len)

    return summary

if __name__=='__main__':
    video_id='EBGb40yh4SY'
    transcript=get_transcript(video_id)
    print(transcript)