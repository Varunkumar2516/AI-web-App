from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

# Import all your functions from backend.py
from backend import (
    ask_chatbot, summarize_text, creative_writer, make_notes, 
    generate_ideas, Text_Translator, Photo_Describer, 
    Code_Explain, Sentiment_Analyzer
)

app = Flask(__name__)
CORS(app) # Allow cross-origin requests

# Define a generic error handler
def handle_request(handler_func, request_data, data_key):
    try:
        if not request_data or data_key not in request_data:
            return jsonify({"error": f"Missing '{data_key}' in request"}), 400
        
        data = request_data[data_key]
        response = handler_func(data)
        return jsonify({"response": response})
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500

@app.route('/api/chatbot', methods=['POST'])
def chatbot_endpoint():
    return handle_request(ask_chatbot, request.json, 'prompt')

@app.route('/api/summarize', methods=['POST'])
def summarize_endpoint():
    return handle_request(summarize_text, request.json, 'text')

@app.route('/api/creative-writer', methods=['POST'])
def writer_endpoint():
    return handle_request(creative_writer, request.json, 'prompt')

@app.route('/api/make-notes', methods=['POST'])
def notes_endpoint():
    return handle_request(make_notes, request.json, 'text')

@app.route('/api/generate-ideas', methods=['POST'])
def ideas_endpoint():
    return handle_request(generate_ideas, request.json, 'prompt')

@app.route('/api/translate', methods=['POST'])
def translate_endpoint():
    return handle_request(Text_Translator, request.json, 'text')

@app.route('/api/explain-code', methods=['POST'])
def code_endpoint():
    return handle_request(Code_Explain, request.json, 'code')

@app.route('/api/sentiment-analyzer', methods=['POST'])
def sentiment_endpoint():
    return handle_request(Sentiment_Analyzer, request.json, 'text')

@app.route('/api/describe-image', methods=['POST'])
def describe_image_endpoint():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Read image bytes directly from the file stream
        image_bytes = file.read()
        description = Photo_Describer(image_bytes)
        return jsonify({"response": description})
    except Exception as e:
        print(f"Error processing image: {e}")
        return jsonify({"error": "An internal server error occurred during image processing"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)