from chatbot.config import ASSISTANT_NAME

conversation_state = {
    "current_flow": "welcome",
    "step": None,
    "data": {}
}

QUICK_ACTIONS = [
    "🚀 Explore Solutions",
    "💬 Ask a Question",
    "📅 Book a Demo",
    "🎫 Technical Support",
    "📞 Contact Our Team"
]

WELCOME_MESSAGE = """
👋 Welcome to CloudRion AI.

I'm here to help you explore our business solutions, answer your questions, connect you with our team, or schedule a personalized demo.

How can I help you today?
"""
