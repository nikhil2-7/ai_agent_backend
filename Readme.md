🚀 AI Agent Pro

AI Agent Pro is a full-stack AI chatbot application built using FastAPI (backend) and Streamlit (frontend). It supports text generation using Groq LLM, image generation using HuggingFace Stable Diffusion, optional web search via Tavily, browser-based voice input, text-to-speech output, and persistent chat history that stores the last 6 conversations without using any SQL database.

✨ Features

🧠 Text generation (Groq – free tier)

🖼 Image generation (HuggingFace Stable Diffusion)

🔍 Optional web search integration

🎙 Voice input (browser microphone)

🔊 AI response speech output

📋 Copy response feature

💾 Persistent history (last 6 conversations only)

⚡ FastAPI backend with Swagger docs

🎨 Modern Streamlit UI

📂 Project Structure
ai_agent.py          # AI logic (LLM + image generation)
backend.py           # FastAPI backend server
frontend.py          # Streamlit frontend UI
history_manager.py   # Stores last 6 conversations
chat_history.json    # Auto-created history file
requirements.txt
.env                 # API keys (not included in repo)
🔑 Environment Variables

Create a .env file in the root folder and add:

GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key
HUGGINGFACE_API_KEY=your_huggingface_key
🐍 Setup Instructions
1️⃣ Create Virtual Environment (Recommended Python 3.10 or 3.11)
python -m venv venv

Activate it:

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate
2️⃣ Install Dependencies
pip install -r requirements.txt
🚀 Run the Application
Start Backend (Terminal 1)
uvicorn backend:app --reload --port 9999

Backend runs at:

http://127.0.0.1:9999

Swagger API docs:

http://127.0.0.1:9999/docs
Start Frontend (Terminal 2)
streamlit run frontend.py

Frontend runs at:

http://localhost:8501

⚠️ Make sure the backend is running before starting the frontend.

🖼 Image Generation

To generate an image, type:

generate image of a futuristic city at night
💾 History System

Stores only the last 6 conversations

Automatically removes the oldest entry when limit exceeds

No database required

Data persists after restart
Conversation history is stored locally in a JSON file and limited to the last 6 interactions for lightweight state management.

📌 Notes

Uses only free-tier services

Do not upload your .env file to GitHub

Recommended Python version: 3.10 or 3.11

👨‍💻 Purpose

This project demonstrates modular AI architecture, API development with FastAPI, frontend integration using Streamlit, agent-based LLM usage, image generation integration, voice interaction, and lightweight persistent memory management.

