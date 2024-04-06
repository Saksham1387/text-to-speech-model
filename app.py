from flask import Flask, request, send_file
from gtts import gTTS
import os
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])
CORS(app, supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'])

@app.route('/speak', methods=['POST'])
def text_to_speech():
    # Retrieve text from the request body
    data = request.json
    text = data.get('text')
    language = data.get('lang', 'en')  # Default to English if no language is provided

    if not text:
        return {"error": "No text provided for conversion."}, 400

    try:
        # Convert text to speech
        speech = gTTS(text=text, lang=language, slow=False)
        # Save the speech to an audio file
        filename = "voice_output.mp3"
        speech.save(filename)

        # Return the generated audio file
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        # Clean up: Remove the audio file after sending it
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == '__main__':
    app.run(port=9090, host='0.0.0.0')
