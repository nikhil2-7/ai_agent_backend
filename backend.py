# ==========================================
# 🚀 BACKEND FILE (FastAPI Server)
# ==========================================

from dotenv import load_dotenv
load_dotenv()

# ==========================================
# 📦 IMPORTS
# ==========================================
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from ai_agent import get_response_from_ai_agent
from history_manager import add_conversation, load_history
from fastapi.middleware.cors import CORSMiddleware



# ==========================================
# 🧾 REQUEST SCHEMA (Input Validation)
# ==========================================
class RequestState(BaseModel):
    model_name: str
    model_provider: str
    system_prompt: str
    messages: List[str]
    allow_search: bool


# ==========================================
# 🧠 ALLOWED FREE MODELS (Groq Only)
# ==========================================
ALLOWED_MODEL_NAMES = [
    "llama3-70b-8192",
    "mixtral-8x7b-32768",
    "llama-3.3-70b-versatile"
]


# ==========================================
# 🌐 FASTAPI APP INITIALIZATION
# ==========================================
app = FastAPI(title="Free LangGraph AI Agent Backend")


# ==========================================
# 💬 CHAT ENDPOINT
# ==========================================
@app.post("/chat")
def chat_endpoint(request: RequestState):
    """
    Main Chat Endpoint
    Handles:
    - Text generation (Groq)
    - Image generation (HuggingFace)
    - Optional web search
    """

    try:
        if request.model_name not in ALLOWED_MODEL_NAMES:
            return {"type": "text", "content": "Invalid model selected."}

        llm_id = request.model_name
        query = request.messages
        allow_search = request.allow_search
        system_prompt = request.system_prompt
        provider = request.model_provider

        # 🔹 Call AI Agent
        response = get_response_from_ai_agent(
            llm_id,
            query,
            allow_search,
            system_prompt,
            provider
        )

        # 🔹 Save Conversation History (Text only)
        user_message = query[0] if isinstance(query, list) else query
        ai_content = response.get("content", "")

        add_conversation(user_message, ai_content)

        return response

    except Exception as e:
        return {
            "type": "text",
            "content": f"❌ Backend Error: {str(e)}"
        }


# ==========================================
# 📜 HISTORY ENDPOINT (Last 6 Conversations)
# ==========================================
@app.get("/history")
def get_chat_history():
    """
    Returns last 6 saved conversations
    """
    return load_history()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 🖥 RUN SERVER DIRECTLY
# ==========================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend:app", host="127.0.0.1", port=9999, reload=True)