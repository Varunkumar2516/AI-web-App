# backend.py
import google.genai as genai
from google.genai import types
import os 
import dotenv 

dotenv.load_dotenv()

Model='models/gemini-2.5-flash'
# Replace with your Gemini API key
API_KEY = os.getenv("APIKEY")
client = genai.Client(api_key=API_KEY)

def ask_chatbot(prompt):
    response = client.models.generate_content(
        model=Model,
        contents=f"Answer as a helpful assistant: {prompt}"
    )
    return response.text

def summarize_text(text):
    response = client.models.generate_content(
        model=Model,
        contents=f"Summarize this text: {text}"
    )
    return response.text

def creative_writer(prompt):
    response = client.models.generate_content(
        model=Model,
        contents=f"Write a creative short story or poem about: {prompt}"
    )
    return response.text

def make_notes(text):
    response = client.models.generate_content(
        model=Model,
        contents=f"Make study notes from this text: {text}"
    )
    return response.text

def generate_ideas(prompt):
    response = client.models.generate_content(
        model=Model,
        contents=f"Generate creative ideas for: {prompt}"
    )
    return response.text

def Text_Translator(text):
    response=client.models.generate_content(
        model=Model,
        contents=f'You have to Change Translate the text Into English ,if user provides the to which language then conver to that one : {text}'
    )
    return response.text

def Code_Explain(code):
    response=client.models.generate_content(
        model=Model,
        contents=f'You have to Explain the Code : which Language ? Which concepts used? which Algorithm is implement ? Its purpose  :{code}'
    )
    return response.text
def Photo_Describer(image):
    try:
        with open(image,'rb') as F:
            image_data=F.read()
        response=client.models.generate_content(
            model=Model,
            contents=[
                types.Part.from_text(text="Describe This image as if Explain to Blind Person"),
                types.Part.from_bytes(data=image_data,mime_type='image/jpeg')
            ]
                
        
        )
        return response.text
    except Exception as e:
        return f'Error in Processing Image:{str(e)}'

def Sentiment_Analyzer(text):
    response=client.models.generate_content(
        model=Model,
        contents=f'You have to Detects positive, neutral, or negative tone in text. :{text}'
    )
    return response.text


import speech_recognition as sr

def speech_to_text():
    """
    Captures audio from the microphone and converts it to text.
    Returns the recognized text or an error message.
    """
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening... Speak now")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
        
        # Convert speech to text using Google Web Speech API (free)
        text = recognizer.recognize_google(audio)
        return text

    except sr.WaitTimeoutError:
        return "No speech detected. Please try again."
    except sr.RequestError:
        return "Could not request results from Google Speech Recognition service."
    except sr.UnknownValueError:
        return "Sorry, could not understand the audio."
