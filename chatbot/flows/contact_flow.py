import re
from chatbot.contact_service import save_contact

contact_sessions = {}


def start_contact(product=None):
    session = {"step": "name"}
    if product:
        session["product"] = product

    return {
        "response": (
            "I'd be happy to connect you with our team. "
            "Let me collect a few details.\n\nMay I have your full name?"
        ),
        "step": "name",
        "product": product,
    }


def create_contact_session(user, product=None):
    contact_sessions[user] = {"step": "name"}
    if product:
        contact_sessions[user]["product"] = product


def save_contact_answer(user, answer):
    if user not in contact_sessions:
        create_contact_session(user)

    step = contact_sessions[user]["step"]

    if step == "name":
        if len(answer.strip()) < 2:
            return "Please enter a valid full name."

        contact_sessions[user]["name"] = answer.strip()
        contact_sessions[user]["step"] = "company"
        return "What is your company name?"

    elif step == "company":
        if len(answer.strip()) < 2:
            return "Please enter a valid company name."

        contact_sessions[user]["company"] = answer.strip()
        contact_sessions[user]["step"] = "email"
        return "Please enter your email address."

    elif step == "email":
        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        if not re.match(pattern, answer.strip()):
            return "Please enter a valid email address."

        contact_sessions[user]["email"] = answer.strip()
        contact_sessions[user]["step"] = "phone"
        return "Please enter your phone number."

    elif step == "phone":
        if len(answer.strip()) < 10:
            return "Please enter a valid phone number."

        contact_sessions[user]["phone"] = answer.strip()
        contact_sessions[user]["step"] = "message"
        return "Please share your message or inquiry."

    elif step == "message":
        if len(answer.strip()) < 5:
            return "Please provide a brief message so our team can assist you."

        contact_sessions[user]["message"] = answer.strip()
        data = contact_sessions[user]

        save_contact(
            data["name"],
            data["company"],
            data["email"],
            data["phone"],
            data["message"],
            data.get("product"),
        )

        del contact_sessions[user]

        return (
            "Thank you! Your message has been sent to our team. "
            "We will get back to you shortly."
        )

    return "Contact request completed."
