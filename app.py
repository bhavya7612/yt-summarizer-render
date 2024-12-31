from flask import Flask, request, render_template, jsonify, session, redirect
import summariser
import video_info

app=Flask(__name__)
app.secret_key='123-456-789'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/project')
def projectpage():
    return render_template('url.html')


@app.route('/output',methods=['GET','POST'])
def summarise():
    if request.method=='POST':
        url=request.form['url']
        max_len=request.form.get('max_len','')
        lang=request.form['lang']
        if not max_len.isdigit():
            max_len=150
        else:
            max_len=int(max_len)
        video_id=url.split('=')[1]
        title=video_info.get_video_title(video_id)
        transcript=summariser.get_transcript(video_id)
        summary=summariser.summarise(video_id, max_len, lang)
        langs={
                'en':'English', 'hi':'Hindi', 'mr':'Marathi',\
                'gu':'Gujarati', 'ml':'malayalam', 'kn':'Kannada',\
                'bn':'Bengali', 'pa':'Punjabi', 'ta':'Tamil',\
                'te':'Telugu', 'ar':'Arabic', 'fr':'French',\
                'de':'German', 'ja':'Japanese', 'ru':'Russian', 'es':'Spanish'}
        # tr_len=len(transcript.split())
        # sum_len=len(summary.split())
        return render_template('output.html', transcript=transcript, summary=summary, title=title, lang=langs[lang])
    else:
        return render_template('output.html')

if __name__=="__main__":
    app.run()