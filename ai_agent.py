from dotenv import load_dotenv
load_dotenv()

# ===============================
# 🔑 API KEYS
# ===============================
import os
import requests
import uuid

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
#HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACE_API_KEY")

# ===============================
# 🤖 LLM SETUP
# ===============================
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

# ===============================
# ✅ IMPORT HISTORY MANAGER
# ===============================
from history_manager import load_history


# ===============================
# 🖼 IMAGE GENERATION (HuggingFace)
# ===============================
# HF_IMAGE_MODEL = "stabilityai/stable-diffusion-2"

# def generate_image(prompt):
#     try:
#         API_URL = f"https://api-inference.huggingface.co/models/{HF_IMAGE_MODEL}"
#         headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
#         payload = {"inputs": prompt}

#         response = requests.post(API_URL, headers=headers, json=payload, timeout=60)

#         if response.status_code == 200:
#             image_bytes = response.content
#             image_name = f"generated_{uuid.uuid4().hex}.png"
#             image_path = os.path.join("generated_images", image_name)

#             os.makedirs("generated_images", exist_ok=True)

#             with open(image_path, "wb") as f:
#                 f.write(image_bytes)

#             return image_path

#         return None

#     except Exception:
#         return None


# ===============================
# 🎙 SPEECH TO TEXT (DISABLED)
# ===============================
# Mic functionality temporarily disabled due to free-tier API limits.
# def speech_to_text(audio_bytes):
#     return None


# ===============================
# 🧠 MAIN AGENT FUNCTION
# ===============================
def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):

    try:
        user_input = query[0] if isinstance(query, list) else query

        # # 🔹 IMAGE REQUEST
        # if user_input.lower().startswith("generate image"):
        #     image_path = generate_image(user_input)

        #     if image_path:
        #         return {
        #             "type": "image",
        #             "content": image_path
        #         }
        #     else:
        #         return {
        #             "type": "text",
        #             "content": "⚠️ Image generation failed."
        #         }

        # 🔹 LLM INITIALIZATION
        llm = ChatGroq(
            model=llm_id,
            api_key=GROQ_API_KEY
        )

        tools = []
        if allow_search and TAVILY_API_KEY:
            tools = [TavilySearchResults(max_results=2)]

        agent = create_react_agent(
            model=llm,
            tools=tools,
        )

        # ✅ ONLY CHANGE — Load history and pass to LLM
        raw_history = load_history()

        # Convert history format {"human": ..., "ai": ...}
        # to LLM format {"role": "user/assistant", "content": ...}
        # History is stored latest first, so reverse it for correct order
        history_messages = []
        for conv in reversed(raw_history):
            history_messages.append({"role": "user", "content": conv["human"]})
            history_messages.append({"role": "assistant", "content": conv["ai"]})

        state = {
            "messages": [
                {"role": "system", "content": system_prompt},
                *history_messages,          # ✅ Last 6 conversations added here
                {"role": "user", "content": user_input}
            ]
        }
        # ✅ END OF CHANGE

        response = agent.invoke(state)

        messages = response.get("messages", [])

        ai_messages = [
            message.content
            for message in messages
            if isinstance(message, AIMessage)
        ]

        if not ai_messages:
            return {
                "type": "text",
                "content": "⚠️ No response generated."
            }

        return {
            "type": "text",
            "content": ai_messages[-1]
        }

    except Exception as e:
        return {
            "type": "text",
            "content": f"❌ AI Agent Error: {str(e)}"
        }