# Daksh : The Personal AI Assistant 🤖

Daksh is a **personal AI assistant** built using **Python, Flask, Speech Recognition, Text‑to‑Speech (TTS), and Large Language Models (LLMs)**. It is designed to interact with users through **voice and text**, intelligently classify user queries, automate basic tasks, and respond conversationally via an AI chatbot engine.

This project demonstrates how modern AI systems can be combined with automation and voice technologies to create a smart, extensible personal assistant.

---

## 🚀 Project Overview

**Daksh** acts as a desktop/web‑based AI assistant capable of:

* Listening to user voice commands
* Converting speech to text
* Understanding the intent of the query
* Responding intelligently using an AI chatbot
* Speaking responses using text‑to‑speech
* Performing basic automation tasks
* Providing a clean web‑based interface

The assistant is modular, making it easy to extend with new features such as OS control, APIs, smart automation, or IoT integrations.

---

## 🧠 Key Features

* 🎤 **Speech Recognition** – Converts voice commands into text
* 🧾 **Query Classification** – Identifies the intent of user queries
* 🤖 **AI Chatbot Integration** – Uses LLMs for intelligent conversation
* 🔊 **Text‑to‑Speech (TTS)** – Converts AI responses into human‑like speech
* 🌐 **Web Interface** – Interactive UI built with HTML, Bootstrap, and JavaScript
* ⚙️ **Automation Support** – Handles browser actions and basic system tasks
* 🧩 **Modular Architecture** – Easy to scale and customize

---

## 🏗️ Project Structure

```
Daksh AI/
│
├── app.py                  # Main Flask application
├── chatbot.py              # AI chatbot logic (LLM integration)
├── query_classifier.py     # Intent classification system
├── speech_handler.py       # Speech recognition module
├── tts.py                  # Text‑to‑speech engine
├── automation.py           # Automation and action handling
├── script.js               # Frontend JavaScript logic
├── .env                    # Environment variables (API keys)
│
├── templates/
│   └── index.html          # Web UI
│
└── Data/
    └── speech.mp3          # Audio output storage
```

---

## ⚙️ Technologies Used

### Backend

* Python 3.9+
* Flask (Web Framework)
* Flask‑CORS
* SpeechRecognition
* pyttsx3 (Offline TTS)
* Groq API / LLM integration
* python‑dotenv

### Frontend

* HTML5
* CSS3
* Bootstrap
* JavaScript

---

## 🔧 Setup & Installation Guide

### 1️⃣ Clone or Extract the Project

```bash
git clone <repository‑url>
cd Daksh-AI
```

Or extract the ZIP file manually.

---

### 2️⃣ Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

---

### 3️⃣ Install Required Dependencies

```bash
pip install flask flask-cors speechrecognition pyttsx3 python-dotenv groq
```

> ⚠️ Make sure you have **PyAudio** installed for speech recognition:

**Windows**

```bash
pip install pipwin
pipwin install pyaudio
```

**Linux**

```bash
sudo apt install portaudio19-dev
pip install pyaudio
```

---

### 4️⃣ Configure Environment Variables

Edit the `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

---

### 5️⃣ Run the Application

```bash
python app.py
```

Open your browser and navigate to:

```
http://127.0.0.1:5000
```

---

## 🧪 How It Works

1. User speaks or types a query
2. Speech is converted to text
3. Query is classified by intent
4. AI chatbot processes the request
5. Response is generated
6. Response is spoken via TTS
7. Result is displayed on the web UI

---

## 🔐 Security Notes

* Do **NOT** expose your `.env` file publicly
* Use API keys responsibly
* Run the assistant locally for maximum privacy

---

## 🚧 Future Enhancements

* OS‑level automation (files, apps, system commands)
* Wake‑word detection
* Multilingual support
* Mobile app integration
* AI memory & personalization
* Offline LLM support
* Smart home & IoT integration

---

## 👨‍💻 Author

**Project Name:** Daksh – The Personal AI Assistant
**Domain:** AI • Voice Assistant • Automation • NLP

---

## 📜 License

This project is intended for **educational and research purposes**. You are free to modify and extend it for personal use.

---

✨ *Daksh is a step toward building your own intelligent AI companion.*
