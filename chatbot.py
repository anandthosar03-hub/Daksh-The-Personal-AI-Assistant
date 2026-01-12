import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class ChatBot:
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY')
        if self.api_key:
            self.client = Groq(api_key=self.api_key)
            self.use_groq = True
        else:
            self.use_groq = False
        
        self.conversation_history = []
        
        # Fallback responses
        self.responses = {
            "what is ai": "Artificial Intelligence (AI) is the simulation of human intelligence in machines that are programmed to think and learn like humans. AI systems can perform tasks such as visual perception, speech recognition, decision-making, and language translation.",
            "artificial intelligence": "AI refers to computer systems that can perform tasks typically requiring human intelligence, such as learning, reasoning, problem-solving, and understanding natural language.",
            "hello": "Hello! I'm Jarvis, your AI assistant. How can I help you today?",
            "hi": "Hi there! What can I do for you?",
            "how are you": "I'm doing great! Thanks for asking. How are you?",
            "what is your name": "I'm Jarvis, your AI assistant.",
            "help": "I can help you with various tasks like answering questions, playing music, telling time, searching the web, sending emails, and more!",
            "bye": "Goodbye! Have a great day!",
            "thank you": "You're welcome! Happy to help!",
            "weather": "I don't have real-time weather data, but you can ask me to search Google for current weather information.",
            "joke": "Why don't scientists trust atoms? Because they make up everything!",
            "what can you do": "I can answer questions, play music on YouTube, tell time and date, open applications, search Google and Wikipedia, send emails, and have conversations with you!",
            "machine learning": "Machine Learning is a subset of AI that enables computers to learn and improve from experience without being explicitly programmed. It uses algorithms to analyze data and make predictions.",
            "python": "Python is a high-level programming language known for its simplicity and readability. It's widely used in web development, data science, AI, and automation.",
            "programming": "Programming is the process of creating instructions for computers to follow. It involves writing code in various languages like Python, JavaScript, Java, and others."
        }
    
    def get_response(self, user_message):
        try:
            user_message = str(user_message).lower().strip()
            
            # Try Groq API first
            if self.use_groq:
                try:
                    self.conversation_history.append({"role": "user", "content": user_message})
                    
                    if len(self.conversation_history) > 10:
                        self.conversation_history = self.conversation_history[-10:]
                    
                    system_message = {
                        "role": "system",
                        "content": "You are Jarvis, an intelligent AI assistant. Be helpful, concise, and friendly. Provide informative answers."
                    }
                    
                    messages = [system_message] + self.conversation_history
                    
                    response = self.client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=messages,
                        temperature=0.7,
                        max_tokens=1024
                    )
                    
                    ai_response = response.choices[0].message.content
                    self.conversation_history.append({"role": "assistant", "content": ai_response})
                    return ai_response
                    
                except Exception as e:
                    print(f"Groq API error: {e}")
                    # Fall back to local responses
                    pass
            
            # Use fallback responses
            for keyword, response in self.responses.items():
                if keyword in user_message:
                    return response
            
            return "I'm here to help! You can ask me questions, request tasks like playing music, checking time, or just have a conversation with me."
            
        except Exception as e:
            print(f"Chatbot error: {e}")
            return "Sorry, I encountered an error. Please try again."
    
    def clear_history(self):
        self.conversation_history = []