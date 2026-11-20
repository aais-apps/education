import frappe
from frappe.translate import get_all_translations

no_cache = 1


def get_context(context):
    context.portal_language = frappe.local.lang
    context.portal_translations = get_all_translations(context.portal_language)
    abbr = frappe.db.get_single_value(
        "Education Settings", "school_college_name_abbreviation"
    )
    logo = frappe.db.get_single_value("Education Settings", "school_college_logo")
    context.abbr = abbr or "Frappe Education"
    context.logo = logo or "/favicon.png"
