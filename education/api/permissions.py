import frappe


def has_app_permission():
    """Check if the user has permission to access the app."""
    if frappe.session.user == "Administrator":
        return True

    if frappe.get_cached_value("User", frappe.session.user, "user_type") != "System User":
        return False

    return bool(
        {"System Manager", "Education Manager", "Instructor", "School Teacher"}
        & set(frappe.get_roles())
    )
