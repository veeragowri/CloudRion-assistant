import re
from chatbot.demo_service import save_demo

# Stores active demo conversations
demo_sessions = {}


def start_demo():
    return {
        "response": (
            "I'd be happy to help you schedule a personalized CloudRion demo.\n\n"
            "May I know your full name?"
        ),
        "step": "name"
    }


def create_demo_session(user):
    demo_sessions[user] = {
        "step": "name"
    }


def get_step(user):
    if user in demo_sessions:
        return demo_sessions[user]["step"]
    return None


def save_answer(user, answer):

    if user not in demo_sessions:
        create_demo_session(user)

    step = demo_sessions[user]["step"]

    # ---------------- NAME ----------------

    if step == "name":

        if len(answer.strip()) < 2:
            return "Please enter a valid full name."

        demo_sessions[user]["name"] = answer.strip()
        demo_sessions[user]["step"] = "company"

        return "Thank you! What is your company name?"

    # ---------------- COMPANY ----------------

    elif step == "company":

        if len(answer.strip()) < 2:
            return "Please enter a valid company name."

        demo_sessions[user]["company"] = answer.strip()
        demo_sessions[user]["step"] = "email"

        return "Please enter your email address.\nExample: abc@gmail.com"

    # ---------------- EMAIL ----------------

    elif step == "email":

        pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

        if not re.match(pattern, answer.strip()):
            return (
                "❌ Invalid email address.\n\n"
                "Example:\n"
                "abc@gmail.com"
            )

        demo_sessions[user]["email"] = answer.strip()
        demo_sessions[user]["step"] = "phone"

        return "Please enter your 10-digit phone number."

    # ---------------- PHONE ----------------

    elif step == "phone":

        if not answer.isdigit() or len(answer) != 10:
            return (
                "❌ Invalid phone number.\n\n"
                "Phone number must contain exactly 10 digits."
            )

        demo_sessions[user]["phone"] = answer
        demo_sessions[user]["step"] = "product"

        return {
            "response": "Which CloudRion product are you interested in?",
            "products": [
                "CloudRion CRM",
                "CloudRion ERP",
                "CloudRion HRMS",
                "CloudRion Billing"
            ]
        }

    # ---------------- PRODUCT ----------------

    elif step == "product":

        valid_products = [
            "cloudrion crm",
            "cloudrion erp",
            "cloudrion hrms",
            "cloudrion billing",
            "cloudrion billing software"
        ]

        if answer.lower() not in valid_products:
            return {
                "response": "Please select one of the products below.",
                "products": [
                    "CloudRion CRM",
                    "CloudRion ERP",
                    "CloudRion HRMS",
                    "CloudRion Billing"
                ]
            }

        demo_sessions[user]["product"] = answer
        demo_sessions[user]["step"] = "datetime"

        return {
            "response": "Please select your preferred demo date and time.",
            "datetime_picker": True
        }

    # ---------------- DATE & TIME ----------------

    elif step == "datetime":

        if len(answer.strip()) < 5:
            return {
                "response": "Please select a valid date and time.",
                "datetime_picker": True
            }

        demo_sessions[user]["preferred_datetime"] = answer.strip()

        data = demo_sessions[user]

        save_demo(
            data["name"],
            data["company"],
            data["email"],
            data["phone"],
            data["product"],
            data["preferred_datetime"]
        )

        del demo_sessions[user]

        return (
            "Thank you! Our team will contact you shortly to schedule your "
            "personalized CloudRion demonstration."
        )

    return "Conversation completed."