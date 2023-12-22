from flask import Flask, send_file, request, jsonify
from gtts import gTTS
import os
import re

app = Flask(__name__)

@app.route('/get-audio/<phrase>', methods=['GET'])
def get_audio(phrase):
    tts = gTTS(phrase, lang='en')  # Set the language as needed
    audio_file = f"{phrase}.mp3"
    tts.save(audio_file)
    return send_file(audio_file, as_attachment=True)

@app.route('/api/process-notes', methods=['POST'])
def process_notes():
    data = request.json
    raw_notes = data.get('notes', '')
    
    # Simple parsing logic (customize as needed)
    # Splitting notes into sentences/phrases using a regular expression
    phrases = re.split(r'[.!?]+', raw_notes)
    phrases = [phrase.strip() for phrase in phrases if phrase.strip()]

    # Structure the data for flashcards
    flashcards = [{'text': phrase} for phrase in phrases]

    return jsonify({'flashcards': flashcards})

if __name__ == '__main__':
    app.run(debug=True)
