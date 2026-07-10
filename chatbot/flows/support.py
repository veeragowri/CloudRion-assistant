import re
from chatbot.ticket_service import save_ticket

support_sessions = {}

PRODUCTS = [
    "CloudRion CRM",
    "CloudRion ERP",
    "CloudRion HRMS",
    "CloudRion Billing",
]


def start_support():
    return {
        "response": "Which CloudRion product do you need help with?",
        "products": PRODUCTS,
        "step": "product",
    }


def create_support_session(user):
    support_sessions[user] = {"step": "product"}


def save_support_answer(user, answer):
    if user not in support_sessions:
        create_support_session(user)

    step = support_sessions[user]["step"]

    if step == "product":
        valid = [p.lower() for p in PRODUCTS]
        if answer.strip().lower() not in valid:
            return {
                "response": "Please select one of the CloudRion products below.",
                "products": PRODUCTS,
            }

        support_sessions[user]["product"] = answer.strip()
        support_sessions[user]["step"] = "issue"
        return "Briefly describe your issue."

    elif step == "issue":
        if len(answer.strip()) < 5:
            return "Please provide a brief description of your issue so we can help you."

        support_sessions[user]["issue"] = answer.strip()
        support_sessions[user]["step"] = "name"
        return (
            "Our technical support team is best equipped to assist you with this request. "
            "I'll collect your details and forward your request to the appropriate team.\n\n"
            "May I have your full name?"
        )

    elif step == "name":
        if len(answer.strip()) < 2:
            return "Please enter a valid full name."

        support_sessions[user]["name"] = answer.strip()
        support_sessions[user]["step"] = "company"
        return "What is your company name?"

    elif step == "company":
        if len(answer.strip()) < 2:
            return "Please enter a valid company name."

        support_sessions[user]["company"] = answer.strip()
        support_sessions[user]["step"] = "email"
        return "Please enter your email address."

    elif step == "email":
        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        if not re.match(pattern, answer.strip()):
            return "Please enter a valid email address."

        support_sessions[user]["email"] = answer.strip()
        support_sessions[user]["step"] = "phone"
        return "Please enter your phone number."

    elif step == "phone":
        if len(answer.strip()) < 10:
            return "Please enter a valid phone number."

        support_sessions[user]["phone"] = answer.strip()
        data = support_sessions[user]

        save_ticket(
            data["name"],
            data["company"],
            data["email"],
            data["phone"],
            data["product"],
            data["issue"],
        )

        del support_sessions[user]

        return (
            "Thank you! Your support request has been forwarded to our technical team. "
            "They will contact you shortly."
        )

    return "Support request completed."
