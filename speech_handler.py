import speech_recognition as sr
import threading

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        
        # Adjust for ambient noise
        try:
            with self.microphone as source:
                print("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Speech recognition ready")
        except Exception as e:
            print(f"Warning: Could not adjust for ambient noise: {e}")
    
    def listen_once(self):
        """Listen for a single command and return the text"""
        try:
            with self.microphone as source:
                print("Listening...")
                # Listen for audio with timeout
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
            print("Recognizing...")
            # Use Google's speech recognition
            text = self.recognizer.recognize_google(audio, language="en-US")
            print(f"You said: {text}")
            return text
            
        except sr.WaitTimeoutError:
            return "Listening timeout - no speech detected"
        except sr.UnknownValueError:
            return "Could not understand audio - please speak clearly"
        except sr.RequestError as e:
            return f"Speech recognition service error: {e}"
        except Exception as e:
            return f"Error: {e}"
    
    def test_microphone(self):
        """Test if microphone is working"""
        try:
            with self.microphone as source:
                print("Testing microphone... Say something!")
                audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=5)
                text = self.recognizer.recognize_google(audio)
                return f"Microphone test successful! You said: {text}"
        except sr.WaitTimeoutError:
            return "Microphone test timeout - no speech detected"
        except sr.UnknownValueError:
            return "Microphone working but could not understand speech"
        except Exception as e:
            return f"Microphone test failed: {e}"