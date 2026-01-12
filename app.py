from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import os
from datetime import datetime
from tts import speak_async
from chatbot import ChatBot
from speech_handler import SpeechRecognizer
from automation import AutomationHandler
from query_classifier import QueryClassifier

app = Flask(__name__)
CORS(app)

# File paths
CONTACTS_FILE = 'contacts.txt'
CHATS_FILE = 'chats.txt'

# Initialize services
try:
    chatbot = ChatBot()
    speech_recognizer = SpeechRecognizer()
    automation = AutomationHandler()
    classifier = QueryClassifier()
    print("All services initialized successfully")
except Exception as e:
    print(f"Error initializing services: {e}")
    chatbot = None
    speech_recognizer = None
    automation = None
    classifier = None

def init_files():
    for file_path in [CONTACTS_FILE, CHATS_FILE]:
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('[]')

def load_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            return json.loads(content) if content else []
    except:
        return []

def save_data(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving to {file_path}: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat/message', methods=['POST'])
def chat_with_bot():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'success': False, 'message': 'No message provided'}), 400
        
        user_message = str(data['message']).strip()
        
        # Classify and route query intelligently
        if classifier:
            strategy = classifier.get_processing_strategy(user_message)
            
            if strategy['handler'] == 'automation' and automation:
                automation_result = automation.process_command(user_message)
                if automation_result['success']:
                    ai_response = automation_result['message']
                else:
                    # Fallback to chatbot
                    ai_response = chatbot.get_response(user_message) if chatbot else "Service unavailable"
            else:
                # Use chatbot first, fallback to automation
                if chatbot:
                    ai_response = chatbot.get_response(user_message)
                elif automation:
                    automation_result = automation.process_command(user_message)
                    ai_response = automation_result['message'] if automation_result['success'] else "Service unavailable"
                else:
                    ai_response = "Service unavailable"
        else:
            # Fallback without classifier
            if automation:
                automation_result = automation.process_command(user_message)
                ai_response = automation_result['message'] if automation_result['success'] else (chatbot.get_response(user_message) if chatbot else "Service unavailable")
            else:
                ai_response = chatbot.get_response(user_message) if chatbot else "Service unavailable"
        
        # Save conversation
        chats = load_data(CHATS_FILE)
        chats.append({
            'type': 'user',
            'message': user_message,
            'timestamp': datetime.now().isoformat()
        })
        chats.append({
            'type': 'assistant',
            'message': ai_response,
            'timestamp': datetime.now().isoformat()
        })
        save_data(CHATS_FILE, chats)
        
        # Speak response
        try:
            speak_async(ai_response)
        except:
            pass
        
        return jsonify({
            'success': True,
            'user_message': user_message,
            'ai_response': ai_response
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'Chat error'}), 500

@app.route('/api/voice-chat', methods=['POST'])
def voice_chat():
    try:
        if not speech_recognizer:
            return jsonify({'success': False, 'message': 'Speech service unavailable'}), 500
        
        # Listen for speech
        recognized_text = speech_recognizer.listen_once()
        
        if "error" in recognized_text.lower() or "timeout" in recognized_text.lower():
            return jsonify({'success': False, 'message': recognized_text})
        
        # Classify and process command intelligently
        if classifier:
            strategy = classifier.get_processing_strategy(recognized_text)
            
            if strategy['handler'] == 'automation' and automation:
                automation_result = automation.process_command(recognized_text)
                if automation_result['success']:
                    ai_response = automation_result['message']
                else:
                    ai_response = chatbot.get_response(recognized_text) if chatbot else "Service unavailable"
            else:
                if chatbot:
                    ai_response = chatbot.get_response(recognized_text)
                elif automation:
                    automation_result = automation.process_command(recognized_text)
                    ai_response = automation_result['message'] if automation_result['success'] else "Service unavailable"
                else:
                    ai_response = "Service unavailable"
        else:
            # Fallback without classifier
            if automation:
                automation_result = automation.process_command(recognized_text)
                ai_response = automation_result['message'] if automation_result['success'] else (chatbot.get_response(recognized_text) if chatbot else "Service unavailable")
            else:
                ai_response = chatbot.get_response(recognized_text) if chatbot else "Service unavailable"
        
        # Save conversation
        chats = load_data(CHATS_FILE)
        chats.append({
            'type': 'user',
            'message': recognized_text,
            'timestamp': datetime.now().isoformat()
        })
        chats.append({
            'type': 'assistant',
            'message': ai_response,
            'timestamp': datetime.now().isoformat()
        })
        save_data(CHATS_FILE, chats)
        
        # Speak response
        try:
            speak_async(ai_response)
        except:
            pass
        
        return jsonify({
            'success': True,
            'recognized_text': recognized_text,
            'ai_response': ai_response
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'Voice chat error'}), 500

@app.route('/api/chats', methods=['GET'])
def get_chats():
    chats = load_data(CHATS_FILE)
    return jsonify(chats)

@app.route('/api/chats', methods=['DELETE'])
def clear_chats():
    save_data(CHATS_FILE, [])
    return jsonify({'success': True, 'message': 'Chat history cleared'})

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    contacts = load_data(CONTACTS_FILE)
    return jsonify(contacts)

@app.route('/api/contacts', methods=['POST'])
def add_contact():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['name', 'phone', 'email']):
            return jsonify({'success': False, 'message': 'Missing fields'}), 400
        
        contacts = load_data(CONTACTS_FILE)
        contact = {
            'name': data['name'],
            'phone': data['phone'],
            'email': data['email'],
            'created_at': datetime.now().isoformat()
        }
        contacts.append(contact)
        save_data(CONTACTS_FILE, contacts)
        return jsonify({'success': True, 'message': 'Contact added'})
    except:
        return jsonify({'success': False, 'message': 'Error adding contact'}), 500

@app.route('/api/contacts/<int:index>', methods=['DELETE'])
def delete_contact(index):
    contacts = load_data(CONTACTS_FILE)
    if 0 <= index < len(contacts):
        contacts.pop(index)
        save_data(CONTACTS_FILE, contacts)
        return jsonify({'success': True, 'message': 'Contact deleted'})
    return jsonify({'success': False, 'message': 'Contact not found'})

@app.route('/api/tts/test')
def test_tts():
    speak_async("Hello! I am Jarvis, your AI assistant. TTS is working perfectly!")
    return jsonify({'success': True, 'message': 'TTS test initiated'})

@app.route('/api/classify', methods=['POST'])
def classify_query():
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'success': False, 'message': 'No query provided'}), 400
        
        query = str(data['query']).strip()
        
        if classifier:
            strategy = classifier.get_processing_strategy(query)
            return jsonify({
                'success': True,
                'query': query,
                'classification': strategy['classification'],
                'recommended_handler': strategy['handler'],
                'fallback_handler': strategy['fallback'],
                'priority': strategy['priority']
            })
        else:
            return jsonify({'success': False, 'message': 'Classifier unavailable'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'message': 'Classification error'}), 500

if __name__ == '__main__':
    init_files()
    print("\n" + "="*50)
    print("🤖 JARVIS AI ASSISTANT STARTING...")
    print("Features:")
    print("  ✅ AI Chatbot (Groq)")
    print("  ✅ Speech Recognition")
    print("  ✅ Text-to-Speech")
    print("  ✅ Voice Commands")
    print("  ✅ Email & Automation")
    print("  ✅ Intelligent Query Routing")
    print("\n🌐 Server: http://localhost:5000")
    print("🔍 Query Classification: /api/classify")
    print("="*50)
    app.run(debug=True, host='127.0.0.1', port=5000)