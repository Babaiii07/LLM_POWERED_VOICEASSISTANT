import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
import os
from gtts import gTTS

load_dotenv()

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")

def voice_input():
    r=sr.Recognizer()
    
    with sr.Microphone() as source:
        print("listening...")
        audio=r.listen(source)
    try:
        text=r.recognize_google(audio)
        print("you said: ", text)
        return text
    except sr.UnknownValueError:
        print("sorry, could not understand the audio")
    except sr.RequestError as e:
        print("could not request result from google speech recognition service: {0}".format(e))
    

def text_to_speech(text):
    tts=gTTS(text=text, lang="en")
    tts.save("speech.mp3")

genai.configure(api_key=GOOGLE_API_KEY)  
model = genai.GenerativeModel(model_name='gemini-pro') 
chat = model.start_chat(history=[])

def llm_model_object(user_text):
    response=chat.send_message(user_text)
    result=response.text
    return result

while True:
    user_input=input("enter the questions")
    response=llm_model_object(user_input)
    print("Bot: ", response)
    if "bye" in user_input.lower():
        break
    
    
    
    