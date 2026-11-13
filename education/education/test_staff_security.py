"""Exercise account administration boundaries with real role permissions."""

import frappe


def run_checks():
	from frappe.core.doctype.user.user import change_password

	original = frappe.session.user
	frappe.db.savepoint("staff_account_security")
	try:
		frappe.set_user("Administrator")
		users = []
		for suffix, roles in (
			("teacher", ["Instructor", "Academics User", "Employee"]),
			("admin", ["System Manager"]),
		):
			user = frappe.get_doc({
				"doctype": "User",
				"email": f"aais-security-{frappe.generate_hash(length=10)}-{suffix}@example.invalid",
				"first_name": suffix,
				"send_welcome_email": 0,
				"roles": [{"role": role} for role in roles],
			}).insert()
			users.append(user.name)
		teacher, admin = users
		frappe.set_user(teacher)
		for target in (admin, "Administrator"):
			for operation in ("read", "write", "delete", "share"):
				assert not frappe.has_permission("User", operation, target), (target, operation)
			try:
				change_password(target, "NotAnAuthorizedPassword!234")
			except frappe.PermissionError:
				pass
			else:
				raise AssertionError("Teacher changed another account's password")
		try:
			visible = frappe.get_list("User", pluck="name", limit_page_length=1000)
		except frappe.PermissionError:
			visible = []
		assert set(visible) <= {teacher}, visible
		own_user = frappe.get_doc("User", teacher)
		own_user.append("roles", {"role": "System Manager"})
		try:
			own_user.save()
		except frappe.PermissionError:
			pass
		assert not frappe.db.exists("Has Role", {"parent": teacher, "role": "System Manager"}), (
			"Teacher could assign a privileged role to their own account"
		)
		for doctype in ("Role", "Role Profile", "Custom DocPerm", "System Settings", "Email Account"):
			assert not frappe.has_permission(doctype, "write"), doctype
		assert not frappe.has_permission("Customer", "read")
		assert frappe.has_permission("Student", "read"), "Academic access was lost"
		frappe.set_user(admin)
		assert frappe.has_permission("User", "read", teacher)
		assert frappe.has_permission("User", "write", teacher)
		print("Staff account security: teacher account isolation and administrator access passed")
	finally:
		frappe.set_user(original)
		frappe.db.rollback(save_point="staff_account_security")
		frappe.clear_cache()
