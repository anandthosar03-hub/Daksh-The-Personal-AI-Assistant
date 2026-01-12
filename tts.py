import pyttsx3
import threading
import os

# Initialize TTS engine
engine = pyttsx3.init()

# Configure voice
voices = engine.getProperty('voices')
if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)  # Use female voice if available
engine.setProperty('rate', 170)  # Speed of speech
engine.setProperty('volume', 0.9)  # Volume level

def speak(text):
    """Synchronous text-to-speech"""
    try:
        print(f"Speaking: {text}")
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"TTS Error: {e}")

def speak_async(text):
    """Asynchronous text-to-speech"""
    def run_tts():
        try:
            print(f"Speaking: {text}")
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")
    
    # Run TTS in separate thread
    thread = threading.Thread(target=run_tts, daemon=True)
    thread.start()

# Test function
if __name__ == "__main__":
    speak("Hello! I am Jarvis, your AI assistant. Text to speech is working perfectly!")