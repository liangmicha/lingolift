from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/get-audio/<phrase>', methods=['GET'])
def get_audio(phrase):
    # Your logic to fetch or generate the audio for the phrase
    # For now, returning a placeholder response
    return jsonify({"message": "Audio for: " + phrase})

if __name__ == '__main__':
    app.run(debug=True)
