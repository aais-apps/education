"""Payment callbacks must never write accounting entries for an unverified payment."""

import types
import unittest
from unittest.mock import MagicMock, patch

import frappe

from education.education import billing


class TestBillingSecurity(unittest.TestCase):
	def test_minor_units_keep_decimals(self):
		self.assertEqual(billing.minor_amount("2200.50"), 220050)

	def test_demo_rejects_checkout_before_contacting_provider(self):
		invoice = types.SimpleNamespace(student="student-a", docstatus=1)
		with (
			patch.object(frappe, "get_doc", return_value=invoice),
			patch.object(billing, "check_permission"),
			patch.object(billing, "online_payments_enabled", return_value=False),
			patch.object(billing, "get_client") as provider,
		):
			with self.assertRaises(frappe.ValidationError):
				billing.get_payment_options("Sales Invoice", "invoice-a", "01712345678")
			provider.assert_not_called()

	def callback(self, *, other_invoice=False, wrong_amount=False, replay=False):
		invoice = types.SimpleNamespace(
			name="invoice-a",
			student="student-a",
			outstanding_amount=10,
			currency="BDT",
			reload=lambda: None,
		)
		client = MagicMock()
		client.order.fetch.return_value = {
			"id": "order-a",
			"notes": {"invoice": "invoice-b" if other_invoice else "invoice-a"},
		}
		client.payment.fetch.return_value = {
			"id": "payment-a",
			"order_id": "order-a",
			"amount": 1 if wrong_amount else 1000,
			"currency": "BDT",
			"status": "captured",
		}
		with (
			patch.object(billing, "authorized_invoice", return_value=invoice),
			patch.object(frappe.db, "sql"),
			patch.object(billing, "get_client", return_value=client),
			patch.object(frappe.db, "exists", return_value=replay),
			patch.object(billing, "get_payment_entry") as accounting,
		):
			response = {
				"razorpay_order_id": "order-a",
				"razorpay_payment_id": "payment-a",
				"razorpay_signature": "signature",
			}
			if other_invoice or wrong_amount:
				with self.assertRaises((frappe.PermissionError, frappe.ValidationError)):
					billing.handle_payment_success(response, "invoice-a", {})
			else:
				self.assertEqual(
					billing.handle_payment_success(response, "invoice-a", {}), {"status": "already_recorded"}
				)
			accounting.assert_not_called()

	def test_signed_order_cannot_pay_a_different_invoice(self):
		self.callback(other_invoice=True)

	def test_wrong_amount_cannot_create_a_payment(self):
		self.callback(wrong_amount=True)

	def test_replayed_callback_does_not_create_a_second_payment(self):
		self.callback(replay=True)

	def test_captured_payment_posts_once_through_the_accounting_service(self):
		invoice = types.SimpleNamespace(
			name="invoice-a", student="student-a", outstanding_amount=10, currency="BDT", reload=lambda: None
		)
		client = MagicMock()
		client.order.fetch.return_value = {"id": "order-a", "notes": {"invoice": "invoice-a"}}
		client.payment.fetch.return_value = {
			"id": "payment-a",
			"order_id": "order-a",
			"amount": 1000,
			"currency": "BDT",
			"status": "captured",
		}
		with (
			patch.object(billing, "authorized_invoice", return_value=invoice),
			patch.object(frappe.db, "sql"),
			patch.object(billing, "get_client", return_value=client),
			patch.object(frappe.db, "exists", return_value=False),
			patch.object(billing, "get_payment_entry") as accounting,
			patch.object(frappe, "get_doc") as record,
			patch.object(billing, "nowdate", return_value="2026-11-13"),
		):
			result = billing.handle_payment_success(
				{
					"razorpay_order_id": "order-a",
					"razorpay_payment_id": "payment-a",
					"razorpay_signature": "signature",
				},
				"invoice-a",
				{},
			)
			self.assertEqual(result, {"status": "recorded"})
			accounting.assert_called_once_with("Sales Invoice", "invoice-a")
			accounting.return_value.insert.assert_called_once()
			accounting.return_value.submit.assert_called_once()
			record.return_value.insert.assert_called_once_with(ignore_permissions=True)


def run_checks():
	result = unittest.TextTestRunner(verbosity=2).run(
		unittest.defaultTestLoader.loadTestsFromTestCase(TestBillingSecurity)
	)
	assert result.wasSuccessful(), "Billing security regression checks failed"
	return {"tests": result.testsRun, "status": "passed"}


def run_privacy_checks():
	"""Check real query and document hooks on two independent fresh-site students."""
	from education.education import api

	original = frappe.session.user
	frappe.db.savepoint("aais_privacy_test")
	try:
		frappe.set_user("Administrator")
		program = frappe.get_doc({"doctype": "Program", "program_name": "AAIS CI Privacy"}).insert()
		year = frappe.get_doc(
			{
				"doctype": "Academic Year",
				"academic_year_name": "AAIS CI 2026",
				"year_start_date": "2026-01-01",
				"year_end_date": "2026-12-31",
			}
		).insert()
		students = []
		for suffix in ("a", "b"):
			email = f"aais-ci-{suffix}@example.invalid"
			frappe.get_doc(
				{
					"doctype": "User",
					"email": email,
					"first_name": suffix,
					"send_welcome_email": 0,
					"user_type": "Website User",
					"roles": [{"role": "Student"}],
				}
			).insert()
			assert frappe.db.get_value("User", email, "user_type") == "Website User"
			student = frappe.get_doc(
				{"doctype": "Student", "first_name": suffix, "student_email_id": email, "user": email}
			).insert()
			enrollment = frappe.get_doc(
				{
					"doctype": "Program Enrollment",
					"student": student.name,
					"program": program.name,
					"academic_year": year.name,
				}
			).insert()
			students.append((email, student.name, enrollment.name))
		user, own_student, own_enrollment = students[0]
		_, other_student, other_enrollment = students[1]
		frappe.set_user(user)
		visible = frappe.get_list("Program Enrollment", pluck="name", limit_page_length=1000)
		assert visible == [own_enrollment], "Another student's enrollment leaked through the generic list API"
		assert not frappe.has_permission("Program Enrollment", "read", other_enrollment), (
			"Direct document access leaked"
		)
		assert api.get_student_profile(own_student)["student"]["name"] == own_student
		try:
			api.get_current_enrollment(other_student)
		except frappe.PermissionError:
			pass
		else:
			raise AssertionError("Cross-student enrollment API access was allowed")
		return {"generic_list": "passed", "direct_document": "passed", "portal_api": "passed"}
	finally:
		frappe.set_user(original)
		frappe.db.rollback(save_point="aais_privacy_test")
