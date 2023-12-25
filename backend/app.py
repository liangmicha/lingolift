import requests
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import json
import re
import gtts
import time

app = Flask(__name__)
CORS(app)  # This enables CORS for your entire Flask app.
openai_api_key = os.getenv("OPENAI_API_KEY")

@app.route('/get-audio/<phrase>', methods=['GET'])
def get_audio(phrase):
    tts = gtts.gTTS(phrase, lang='pt')  # Adjust the language as needed
    audio_file = f"{phrase}.mp3"
    tts.save(audio_file)
    return send_file(audio_file, as_attachment=True)


@app.route('/api/process-notes', methods=['POST'])
def process_notes():
    data = request.json
    raw_text = data['text']
    learning_language = data['learning_language']
    primary_language = data['primary_language']
    
    # Define the API endpoint
    endpoint = "https://api.openai.com/v1/chat/completions"
    
    # Define the request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }
    
    # Define the request payload
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that translates notes into flashcards."},
            {"role": "user", "content": f"I am learning {learning_language} and my primary language is {primary_language}."},
            {"role": "user", "content": "Here are raw notes I took from a class. Take these raw notes and help me structure them into flashcards that I can study. Do not make flashcards for anything that is not in the learning language. Sometimes I take notes in the primary language, either omit them, or translate them to the learning langauge first. No learning_language_text in the response should be in the primary language. Omit anything that looks like just grammar or notes that are symbols or notes that do not make sense. Correct any typos in either language. If I forgot to put accents on the letter when they should be there, please correct them too before returning. Sometimes I put english in parenthesis, do not include that."},
            {"role": "user", "content": f"""
                Specifically, the flashcard structure would look something like:
                        {{
                            flashcards: [
                                {{ 
                                    learning_language_text: "elas falam sobre tarefas",  
                                    primary_language_text: "They talk about tasks"
                                }},
                                ...
                            ]
                        }}

                        Here is the dump of the raw notes:
                        {raw_text}
            """
            },
            {"role": "user", "content": "here's the raw text: \n" + raw_text}
        ],
        "temperature": 0.7
    }
    
    if False:
        time.sleep(5)
        flashcards_dict = {
            "flashcards": [
                {
                "learning_language_text": "trabalhei",
                "primary_language_text": "I worked"
                },
                {
                "learning_language_text": "desde",
                "primary_language_text": "since"
                },
                {
                "learning_language_text": "desde às seis da manhã",
                "primary_language_text": "since six in the morning"
                }
            ]
        }
        return jsonify({'flashcards': flashcards_dict})
    # Make the API call
    response = requests.post(endpoint, headers=headers, json=payload)
    
    # Check if the API call was successful
    if response.status_code == 200:
        api_response = response.json()
        message_content = api_response['choices'][0]['message']['content']

        # Extract JSON string using regular expression
        match = re.search(r'\{.*\}', message_content, re.DOTALL)
        if match:
            json_string = match.group(0)

            try:
                # Parse the JSON string into a dictionary
                print(json_string)
                flashcards_dict = json.loads(json_string)
                return jsonify({'flashcards': flashcards_dict})
            except json.JSONDecodeError as e:
                print("error " + e.toString())
                return jsonify({'error': 'Extracted string is not valid JSON'}), 400
        else:
            return jsonify({'error': 'No JSON data found in the response'}), 400
    else:
        return jsonify({'error': 'API request failed'}), response.status_code


if __name__ == '__main__':
    app.run(debug=True)
