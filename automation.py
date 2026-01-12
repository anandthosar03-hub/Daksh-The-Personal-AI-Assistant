import pyttsx3
import webbrowser
import datetime
import pyautogui
import wikipedia
import pywhatkit as pwk
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

class AutomationHandler:
    def __init__(self):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        if len(voices) > 1:
            self.engine.setProperty('voice', voices[1].id)
        self.engine.setProperty('rate', 170)
        
        # Email config
        self.gmail_password = os.getenv('gmail_app_password')
        
    def speak(self, text):
        print(f"Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
        
    def process_command(self, command):
        command = str(command).lower().strip()
        
        try:
            # Real-time queries - Time
            if any(phrase in command for phrase in ["what time", "current time", "time now", "what's the time"]):
                now_time = datetime.datetime.now().strftime("%I:%M %p")
                response = f"The current time is {now_time}"
                return {"success": True, "message": response, "type": "realtime"}
                
            # Real-time queries - Date
            elif any(phrase in command for phrase in ["what date", "today's date", "current date", "what day", "today"]):
                now_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
                response = f"Today is {now_date}"
                return {"success": True, "message": response, "type": "realtime"}
                
            # Automation - YouTube music
            elif "play" in command and "youtube" in command:
                search_query = command.replace("play", "").replace("on youtube", "").replace("youtube", "").strip()
                if search_query:
                    pwk.playonyt(search_query)
                    response = f"Playing {search_query} on YouTube"
                    return {"success": True, "message": response, "type": "automation"}
                
            # Automation - Open applications
            elif any(word in command for word in ["open", "launch", "start", "run"]):
                app_name = command
                for word in ["open", "launch", "start", "run"]:
                    app_name = app_name.replace(word, "").strip()
                if app_name:
                    pyautogui.press("super")
                    pyautogui.typewrite(app_name)
                    pyautogui.sleep(1)
                    pyautogui.press("enter")
                    response = f"Opening {app_name}"
                    return {"success": True, "message": response, "type": "automation"}
                    
            # Real-time - Wikipedia search
            elif "wikipedia" in command or "wiki" in command:
                search_term = command.replace("wikipedia", "").replace("wiki", "").replace("search", "").strip()
                if search_term:
                    try:
                        result = wikipedia.summary(search_term, sentences=2)
                        response = f"According to Wikipedia: {result}"
                        return {"success": True, "message": response, "type": "realtime"}
                    except:
                        response = f"Sorry, I couldn't find information about {search_term} on Wikipedia"
                        return {"success": True, "message": response, "type": "realtime"}
                        
            # Automation - Google search
            elif any(phrase in command for phrase in ["search google", "google search", "search for", "look up"]):
                search_term = command
                for phrase in ["search google", "google search", "search for", "look up", "google"]:
                    search_term = search_term.replace(phrase, "").strip()
                if search_term:
                    webbrowser.open(f"https://www.google.com/search?q={search_term}")
                    response = f"Searching Google for {search_term}"
                    return {"success": True, "message": response, "type": "automation"}
                    
            # Automation - Send email
            elif "send email" in command or "email" in command:
                result = self.send_email()
                result["type"] = "automation"
                return result
                
            # Real-time - Weather
            elif "weather" in command:
                webbrowser.open("https://www.google.com/search?q=weather")
                response = "Opening current weather information"
                return {"success": True, "message": response, "type": "realtime"}
                
            # Real-time - News
            elif "news" in command:
                webbrowser.open("https://news.google.com")
                response = "Opening latest news"
                return {"success": True, "message": response, "type": "realtime"}
                
            # Automation - Calculator
            elif "calculate" in command or "math" in command:
                pyautogui.press("super")
                pyautogui.typewrite("calculator")
                pyautogui.sleep(1)
                pyautogui.press("enter")
                response = "Opening calculator"
                return {"success": True, "message": response, "type": "automation"}
                
            else:
                return {"success": False, "message": "Command not recognized", "type": "unknown"}
                
        except Exception as e:
            print(f"Automation error: {e}")
            return {"success": False, "message": "Sorry, I encountered an error"}
    
    def send_email(self):
        try:
            if not self.gmail_password:
                return {"success": True, "message": "Email functionality requires Gmail app password configuration"}
            
            # Default email for demo
            sender_email = "akashdandale123@gmail.com"
            receiver_email = "darshanthorbole@gmail.com"
            
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = "Message from Jarvis AI Assistant"
            
            body = """Hello,

This is an automated message sent from Jarvis AI Assistant.

Best regards,
Jarvis AI Assistant"""
            
            message.attach(MIMEText(body, "plain"))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, self.gmail_password)
            text = message.as_string()
            server.sendmail(sender_email, receiver_email, text)
            server.quit()
            
            return {"success": True, "message": "Email sent successfully"}
            
        except Exception as e:
            print(f"Email error: {e}")
            return {"success": True, "message": "Email service is currently unavailable"}