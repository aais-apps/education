"""Complete the existing AAIS showcase without deleting records or resetting passwords."""

import frappe
from frappe.utils import today


def complete_demo():
	if not frappe.conf.get("demo_site"):
		frappe.throw("This command is restricted to an explicitly configured demo site")
	frappe.only_for("System Manager")
	company = "AAIS"
	program = "Class 10 (Science)"
	year = "2026"
	company_doc = frappe.get_doc("Company", company)
	term = frappe.db.get_value(
		"Academic Term",
		{"academic_year": year, "term_start_date": ["<=", today()], "term_end_date": [">=", today()]},
		"name",
	)
	if not term:
		frappe.throw("No current academic term exists; refusing to guess demo dates")
	settings = frappe.get_single("Education Settings")
	settings.current_academic_year = year
	settings.current_academic_term = term
	settings.save()
	builder_settings = frappe.get_single("Builder Settings")
	if "aais-demo-marker" not in (builder_settings.body_html or ""):
		builder_settings.body_html = (
			(builder_settings.body_html or "")
			+ '<div id="aais-demo-marker" role="note" style="position:fixed;bottom:12px;right:12px;z-index:9999;padding:8px 12px;border:1px solid #d1d5db;border-radius:8px;background:#fff;color:#374151;font:14px/1.5 sans-serif;box-shadow:0 2px 8px #0002">ডেমো • নমুনা তথ্য</div>'
		)
	if 'name="robots"' not in (builder_settings.head_html or ""):
		builder_settings.head_html = (
			builder_settings.head_html or ""
		) + '<meta name="robots" content="noindex,nofollow">'
	builder_settings.save()

	structure_name = frappe.db.get_value("Fee Structure", {"program": program, "academic_year": year}, "name")
	if not structure_name:
		frappe.throw("Create the demo Fee Structure before running completion")
	structure = frappe.get_doc("Fee Structure", structure_name)
	if structure.docstatus == 0:
		structure.submit()
	group = frappe.db.get_value("Student Group", {"program": program, "academic_year": year}, "name")
	if not group:
		frappe.throw("Demo student group not found")
	schedule_name = frappe.db.get_value(
		"Fee Schedule", {"fee_structure": structure_name, "posting_date": "2026-11-01"}, "name"
	)
	if not schedule_name:
		schedule = frappe.get_doc(
			{
				"doctype": "Fee Schedule",
				"fee_structure": structure_name,
				"program": program,
				"academic_year": year,
				"posting_date": "2026-11-01",
				"due_date": "2026-11-25",
				"company": company,
				"currency": "BDT",
				"receivable_account": company_doc.default_receivable_account,
				"cost_center": company_doc.cost_center,
				"send_email": 0,
				"student_groups": [{"student_group": group}],
				"components": [
					{"fees_category": row.fees_category, "amount": row.amount, "total": row.amount}
					for row in structure.components
				],
			}
		).insert()
		schedule.submit()
		schedule_name = schedule.name

	schedule = frappe.get_doc("Fee Schedule", schedule_name)
	if schedule.docstatus == 0:
		schedule.submit()

	students = frappe.get_all(
		"Student", filters={"user": ["like", "student.%@paradox-bd.com"]}, fields=["name", "customer", "user"]
	)
	created = []
	for student in students:
		existing = frappe.db.get_value(
			"Sales Invoice",
			{"student": student.name, "fee_schedule": schedule_name, "docstatus": ["!=", 2]},
			"name",
		)
		if existing:
			invoice = frappe.get_doc("Sales Invoice", existing)
		else:
			invoice = frappe.get_doc(
				{
					"doctype": "Sales Invoice",
					"customer": student.customer,
					"student": student.name,
					"fee_schedule": schedule_name,
					"company": company,
					"set_posting_time": 1,
					"posting_date": "2026-11-01",
					"due_date": "2026-11-25",
					"debit_to": company_doc.default_receivable_account,
					"remarks": "AAIS showcase: November 2026 school fees (demo)",
					"items": [
						{
							"item_code": "FEE-SEC-10",
							"qty": 1,
							"rate": structure.total_amount,
							"income_account": company_doc.default_income_account,
							"cost_center": company_doc.cost_center,
						}
					],
				}
			).insert()
			created.append(invoice.name)
		if invoice.docstatus == 0:
			invoice.submit()
		if (
			student.user in ["student.tanvir@paradox-bd.com", "student.fatima@paradox-bd.com"]
			and invoice.outstanding_amount
			and invoice.name in created
		):
			from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry

			payment = get_payment_entry("Sales Invoice", invoice.name, bank_account="Cash - AAIS")
			payment.posting_date = "2026-11-10"
			payment.reference_date = "2026-11-10"
			payment.reference_no = "AAIS-DEMO-" + invoice.name
			payment.insert()
			payment.submit()
	# Keep the showcase's newer Tanvir bill unpaid. Reverse only a payment made
	# by this completion script; existing/manual payments are never touched.
	tanvir = frappe.db.get_value("Student", {"user": "student.tanvir@paradox-bd.com"}, "name")
	bills = frappe.get_all(
		"Sales Invoice",
		filters={"student": tanvir, "fee_schedule": schedule_name, "docstatus": 1},
		fields=["name"],
		order_by="posting_date asc, creation asc",
	)
	for bill in bills[1:]:
		for payment_name in frappe.get_all(
			"Payment Entry", filters={"reference_no": "AAIS-DEMO-" + bill.name, "docstatus": 1}, pluck="name"
		):
			frappe.get_doc("Payment Entry", payment_name).cancel()
	if students:
		frappe.db.set_value("Fee Schedule", schedule_name, "status", "Invoice Created")
	# Modern fee invoices own the ledger. Creating submitted legacy Fees as well
	# would charge each student a second time.
	return {"created_invoices": created, "fee_schedule": schedule_name, "current_term": term}


def verify_access():
	"""Exercise real ORM list/document permissions against the existing demo records."""
	if not frappe.conf.get("demo_site"):
		frappe.throw("Demo verification requires demo_site")
	from education.education import api
	from education.permissions import STUDENT_DOCUMENTS, allowed_students

	original = frappe.session.user
	results = []
	try:
		users = frappe.get_all(
			"User", filters={"enabled": 1, "user_type": "Website User", "name": ["!=", "Guest"]}, pluck="name"
		)
		all_students = frappe.get_all("Student", pluck="name")
		for user in users:
			frappe.set_user(user)
			allowed = allowed_students(user)
			for doctype in STUDENT_DOCUMENTS:
				try:
					rows = frappe.get_list(doctype, fields=["name", "student"], limit_page_length=1000)
				except frappe.PermissionError:
					assert doctype not in (
						"Assessment Result",
						"Program Enrollment",
						"Student Attendance",
						"Sales Invoice",
					)
					rows = []
				assert all(row.student in allowed for row in rows), (user, doctype, "list leak")
				for student in set(all_students) - allowed:
					name = frappe.db.get_value(doctype, {"student": student}, "name")
					if name:
						assert not frappe.has_permission(doctype, "read", name), (
							user,
							doctype,
							"document leak",
						)
			for student in set(all_students) - allowed:
				for method in [api.get_student_profile, api.get_student_invoices, api.get_current_enrollment]:
					try:
						method(student)
					except frappe.PermissionError:
						pass
					else:
						raise AssertionError((method.__name__, "cross-student access"))
			if "Guardian" in frappe.get_roles():
				assert {row["student"] for row in api.get_guardian_students()} == allowed
			for student in allowed:
				profile = api.get_student_profile(student)
				assert profile["student"]["name"] == student
				assert api.get_student_invoices(student)["invoices"], "Demo invoices missing"
			results.append(
				{
					"type": "guardian" if "Guardian" in frappe.get_roles() else "student",
					"student_count": len(allowed),
					"status": "passed",
				}
			)
	finally:
		frappe.set_user(original)
	return results
