from flask import Flask, send_file
from gtts import gTTS
import os

app = Flask(__name__)

@app.route('/get-audio/<phrase>', methods=['GET'])
def get_audio(phrase):
    tts = gTTS(phrase, lang='en')  # Set the language as needed
    audio_file = f"{phrase}.mp3"
    tts.save(audio_file)
    return send_file(audio_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
