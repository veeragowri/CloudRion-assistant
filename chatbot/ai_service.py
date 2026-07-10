import os
from dotenv import load_dotenv
from groq import Groq

from chatbot.memory import conversation_history

load_dotenv()

_client = None


def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not configured. "
                "Add it in Vercel Project Settings → Environment Variables."
            )
        _client = Groq(api_key=api_key)
    return _client


def get_response(user_message, service=None):
    content = user_message
    if service == "question":
        content = f"[User is asking a question about CloudRion products] {user_message}"
    elif service == "support":
        content = f"[User needs technical support] {user_message}"

    conversation_history.append({
        "role": "user",
        "content": content
    })

    try:
        chat_completion = get_client().chat.completions.create(
            messages=conversation_history,
            model="llama-3.3-70b-versatile",
            temperature=0.7
        )
    except RuntimeError as exc:
        return str(exc)
    except Exception:
        return (
            "I'm having trouble reaching the AI service right now. "
            "Please try again in a moment, or use Book a Demo / Contact Our Team."
        )

    assistant_reply = chat_completion.choices[0].message.content

    conversation_history.append({
        "role": "assistant",
        "content": assistant_reply
    })

    return assistant_reply
