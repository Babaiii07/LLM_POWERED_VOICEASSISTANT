
import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
import os
from gtts import gTTS
import streamlit as st

load_dotenv()

def voice_input():
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = r.listen(source, timeout=5) 
            text = r.recognize_google(audio)
            print("You said:", text)
            return text
        except sr.WaitTimeoutError:
            print("Timeout! No response received within 5 seconds.")
        except sr.UnknownValueError:
            print("Sorry, could not understand the audio.")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service: {0}".format(e))

def text_to_speech(text):
    tts=gTTS(text=text, lang="en")
    tts.save("speech.mp3")



def main():
    st.title("Multilingual AI Assistant 🤖")
    GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=GOOGLE_API_KEY)  
    model = genai.GenerativeModel(model_name='gemini-1.5-pro') 
    chat = model.start_chat(history=[])
    def llm_model_object(user_text):
        response=chat.send_message(user_text)
        result=response.text
        return result
    if st.button("Ask me anything"):
        with st.spinner("Listening..."):
            text=voice_input()
            response=llm_model_object(text)
            text_to_speech(response)
            
            
            audio_file=open("speech.mp3","rb")
            audio_bytes=audio_file.read()
            
            
            st.text_area(label="Response:",value=response,height=350)
            st.audio(audio_bytes)
            st.download_button(label="Download Speech",
                               data=audio_bytes,
                               file_name="speech.mp3",
                               mime="audio/mp3")
if __name__ == "__main__":    
    main()

