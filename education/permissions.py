"""Apply student ownership to generic REST/list/print access as well as portal APIs."""

import frappe

STUDENT_DOCUMENTS = (
	"Assessment Result",
	"Program Enrollment",
	"Course Enrollment",
	"Student Attendance",
	"Fees",
	"Sales Invoice",
	"Student Leave Application",
)


def is_website_user(user):
	return user != "Administrator" and frappe.db.get_value("User", user, "user_type") == "Website User"


def allowed_students(user):
	from education.education.api import get_guardians_for_user

	students = frappe.get_all("Student", filters={"user": user}, pluck="name")
	guardians = get_guardians_for_user(user)
	if guardians:
		students += frappe.get_all(
			"Student Guardian",
			filters={"guardian": ["in", guardians], "parenttype": "Student"},
			pluck="parent",
		)
	return set(students)


def query_conditions(user=None, doctype=None):
	user = user or frappe.session.user
	if not is_website_user(user):
		return ""
	if doctype == "Guardian":
		from education.education.api import get_guardians_for_user

		guardians = get_guardians_for_user(user)
		values = ",".join(frappe.db.escape(guardian) for guardian in guardians)
		return f"`tabGuardian`.`name` IN ({values})" if values else "1=0"
	students = allowed_students(user)
	if not students or doctype == "Student Group":
		return "1=0"
	values = ",".join(frappe.db.escape(student) for student in students)
	if doctype == "Course Schedule":
		return f"`tabCourse Schedule`.`student_group` IN (SELECT parent FROM `tabStudent Group Student` WHERE student IN ({values}) AND parenttype='Student Group')"
	if doctype not in STUDENT_DOCUMENTS:
		return "1=0"
	return f"`tab{doctype}`.`student` IN ({values})"


def has_permission(doc, ptype=None, user=None, debug=False):
	user = user or frappe.session.user
	if not is_website_user(user):
		return True
	if doc.doctype == "Guardian":
		from education.education.api import get_guardians_for_user

		return ptype in (None, "read", "print", "select") and doc.name in get_guardians_for_user(user)
	students = allowed_students(user)
	if doc.doctype == "Student Group":
		return False
	if doc.doctype == "Course Schedule":
		return ptype in (None, "read", "print", "select") and bool(
			frappe.db.exists(
				"Student Group Student",
				{
					"parent": doc.student_group,
					"parenttype": "Student Group",
					"student": ["in", list(students)],
				},
			)
		)
	if doc.get("student") not in students:
		return False
	if doc.doctype == "Student Leave Application":
		return ptype in (None, "read", "print", "select", "create", "write")
	return ptype in (None, "read", "print", "select")
