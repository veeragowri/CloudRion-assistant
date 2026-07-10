EXPLORE_INTRO = (
    "Here are our available CloudRion solutions:\n\n"
    "• CloudRion CRM\n"
    "• CloudRion ERP\n"
    "• CloudRion HRMS\n"
    "• CloudRion Billing\n\n"
    "Select a product to learn more."
)

PRODUCTS = {
    "CloudRion CRM": {
        "pitch": (
            "CloudRion CRM is designed to help businesses streamline customer "
            "management and sales operations. I'd be happy to explain how it fits "
            "your business needs or arrange a personalized demo."
        ),
        "description": "CloudRion CRM helps businesses manage customer relationships and sales operations efficiently.",
        "details": (
            "CloudRion CRM helps businesses manage leads, customer interactions, "
            "sales pipelines, follow-ups, and reporting. It improves productivity "
            "and enhances customer engagement."
        ),
    },
    "CloudRion ERP": {
        "pitch": (
            "CloudRion ERP is designed to support core business operations, "
            "including inventory management. The exact workflow depends on your "
            "business requirements. I can arrange a demo where our team can walk "
            "you through the solution."
        ),
        "description": "CloudRion ERP helps organizations manage core business operations including inventory, finance, and procurement.",
        "details": (
            "CloudRion ERP integrates inventory, finance, procurement, production, "
            "and business operations into one centralized platform."
        ),
    },
    "CloudRion HRMS": {
        "pitch": (
            "CloudRion HRMS simplifies employee management, payroll, attendance, "
            "and HR processes. I'd be happy to explain how it fits your organization "
            "or arrange a personalized demo."
        ),
        "description": "CloudRion HRMS simplifies employee management, payroll, attendance, and HR processes.",
        "details": (
            "CloudRion HRMS manages employee records, attendance, leave, payroll, "
            "recruitment, and performance management efficiently."
        ),
    },
    "CloudRion Billing": {
        "pitch": (
            "CloudRion Billing streamlines invoicing, billing, and payment "
            "management. I'd be happy to explain how it fits your business needs "
            "or arrange a personalized demo."
        ),
        "description": "CloudRion Billing streamlines invoicing, billing, and payment management.",
        "details": (
            "CloudRion Billing helps businesses generate invoices, manage payments, "
            "track transactions, and maintain billing records."
        ),
    },
}


def get_products():
    return list(PRODUCTS.keys())


def get_explore_intro():
    return EXPLORE_INTRO


def get_product_details(product):
    if not product:
        return None
    return PRODUCTS.get(product) or PRODUCTS.get(product.strip())
