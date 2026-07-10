import os
from dotenv import load_dotenv
from groq import Groq

from chatbot.memory import conversation_history

# Load .env file
load_dotenv()

# Create Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

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

    # Send the entire conversation to Groq
    chat_completion = client.chat.completions.create(
        messages=conversation_history,
        model="llama-3.3-70b-versatile",
        temperature=0.7
    )

    # Get AI response
    assistant_reply = chat_completion.choices[0].message.content

    # Save AI response
    conversation_history.append({
        "role": "assistant",
        "content": assistant_reply
    })

    return assistant_reply