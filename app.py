from chatbot.config import CONTACT_INFO
from chatbot.conversation import WELCOME_MESSAGE, QUICK_ACTIONS
from chatbot.ticket_service import save_ticket
from database.database import create_database
from flask import Flask, render_template, request, jsonify
from chatbot.ai_service import get_response
from chatbot.flows.explore import get_products, get_product_details, get_explore_intro
from chatbot.flows.demo import (
    create_demo_session,
    save_answer,
    start_demo,
    demo_sessions,
)
from chatbot.flows.support import (
    create_support_session,
    save_support_answer,
    start_support,
    support_sessions,
)
from chatbot.flows.contact_flow import (
    create_contact_session,
    save_contact_answer,
    start_contact,
    contact_sessions,
)

app = Flask(__name__)

# Ensure SQLite tables exist (uses /tmp on Vercel when needed)
try:
    create_database()
except Exception:
    pass

QUESTION_FOLLOW_UP = (
    "\n\nIf you'd like, I can arrange a personalized demo where our team "
    "can show how CloudRion fits your business requirements."
)

QUESTION_BUTTONS = [
    {"label": "📅 Book Demo", "action": "book_demo"},
    {"label": "💬 Continue Asking", "action": "continue_asking"},
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/welcome")
def welcome():
    return jsonify({
        "message": WELCOME_MESSAGE,
        "actions": QUICK_ACTIONS,
    })


@app.route("/products")
def products():
    return jsonify({
        "intro": get_explore_intro(),
        "products": get_products(),
    })


@app.route("/product/<product_name>")
def product_details(product_name):
    product = get_product_details(product_name)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)


@app.route("/contact")
def contact():
    return jsonify({
        "message": CONTACT_INFO,
    })


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    service = data.get("service")
    user_message = data.get("message")

    response = get_response(user_message, service=service)

    result = {"response": response}

    if service == "question":
        if QUESTION_FOLLOW_UP.strip() not in response:
            result["response"] = response + QUESTION_FOLLOW_UP
        result["buttons"] = QUESTION_BUTTONS

    return jsonify(result)


@app.route("/raise-ticket", methods=["POST"])
def raise_ticket():
    data = request.get_json()

    save_ticket(
        data["name"],
        data.get("company", ""),
        data["email"],
        data["phone"],
        data["product"],
        data["issue"],
    )

    return jsonify({
        "message": (
            "Thank you! Your support request has been forwarded to our technical team. "
            "They will contact you shortly."
        ),
    })


@app.route("/book-demo", methods=["POST"])
def book_demo():
    data = request.get_json()

    from chatbot.demo_service import save_demo

    save_demo(
        data["name"],
        data["company"],
        data["email"],
        data["phone"],
        data["product"],
        data["preferred_datetime"],
    )

    return jsonify({
        "message": (
            "Thank you! Our team will contact you shortly to schedule your "
            "personalized CloudRion demonstration."
        ),
    })


@app.route("/demo", methods=["POST"])
def demo():
    data = request.get_json()
    user = "demo_user"
    message = (data.get("message") or "").strip()

    if data.get("start"):
        if user in demo_sessions:
            del demo_sessions[user]
        create_demo_session(user)
        return jsonify(start_demo())

    if user not in demo_sessions:
        create_demo_session(user)
        return jsonify(start_demo())

    if not message:
        return jsonify(start_demo())

    reply = save_answer(user, message)

    if isinstance(reply, dict):
        return jsonify(reply)

    return jsonify({"response": reply})


@app.route("/support", methods=["POST"])
def support():
    data = request.get_json()
    user = "support_user"
    message = (data.get("message") or "").strip()

    if data.get("start"):
        if user in support_sessions:
            del support_sessions[user]
        create_support_session(user)
        return jsonify(start_support())

    if user not in support_sessions:
        create_support_session(user)
        return jsonify(start_support())

    if not message:
        return jsonify(start_support())

    reply = save_support_answer(user, message)

    if isinstance(reply, dict):
        return jsonify(reply)

    return jsonify({"response": reply})


@app.route("/contact-flow", methods=["POST"])
def contact_flow():
    data = request.get_json()
    user = "contact_user"
    message = (data.get("message") or "").strip()
    product = data.get("product")

    if data.get("start"):
        if user in contact_sessions:
            del contact_sessions[user]
        create_contact_session(user, product=product)
        return jsonify(start_contact(product=product))

    if user not in contact_sessions:
        create_contact_session(user, product=product)
        return jsonify(start_contact(product=product))

    if not message:
        return jsonify(start_contact(product=product))

    reply = save_contact_answer(user, message)

    if isinstance(reply, dict):
        return jsonify(reply)

    return jsonify({"response": reply})


if __name__ == "__main__":
    create_database()
    app.run(debug=True)
