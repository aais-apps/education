"""Optional Razorpay checkout. Demo sites never initiate real payments."""
from decimal import ROUND_HALF_UP, Decimal

import frappe
from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry
from frappe import _
from frappe.utils import nowdate, validate_phone_number

from education.education.api import check_permission


def online_payments_enabled():
    return bool(not frappe.conf.get("demo_site") and frappe.conf.get("enable_education_online_payments"))


def minor_amount(amount):
    return int((Decimal(str(amount)) * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def authorized_invoice(name):
    invoice = frappe.get_doc("Sales Invoice", name)
    check_permission(invoice.student, "invoice payment")
    if invoice.docstatus != 1:
        frappe.throw(_("Only submitted invoices can be paid"))
    if not online_payments_enabled():
        frappe.throw(_("Online payments are disabled. Please contact the school office."))
    return invoice


def get_client():
    import razorpay
    settings = frappe.get_single("Education Settings")
    key = settings.razorpay_key
    secret = settings.get_password("razorpay_secret", raise_exception=False)
    if not key or not secret:
        frappe.throw(_("Online payment is not configured. Please contact the school office."))
    return razorpay.Client(auth=(key, secret))


@frappe.whitelist()
def get_payment_options(doctype: str, docname: str, phone: str, currency: str | None = None):
    if doctype != "Sales Invoice":
        raise frappe.PermissionError(_("Unsupported payment document"))
    invoice = authorized_invoice(docname)
    if invoice.outstanding_amount <= 0:
        frappe.throw(_("This invoice has no outstanding balance"))
    validate_phone_number(phone_number=phone, throw=True)
    client = get_client()
    order = client.order.create({
        "amount": minor_amount(invoice.outstanding_amount), "currency": invoice.currency,
        "notes": {"invoice": invoice.name},
    })
    return {
        "key": frappe.db.get_single_value("Education Settings", "razorpay_key"),
        "name": frappe.db.get_single_value("Website Settings", "app_name"),
        "description": _("School fees"), "order_id": order["id"],
        "amount": order["amount"], "currency": order["currency"],
        "prefill": {"email": frappe.session.user, "contact": phone},
    }


@frappe.whitelist()
def handle_payment_success(response: dict, against_invoice: str, billing_details: dict):
    invoice = authorized_invoice(against_invoice)
    # Serialize callbacks for one invoice, including retries from different tabs.
    frappe.db.sql("SELECT name FROM `tabSales Invoice` WHERE name=%s FOR UPDATE", invoice.name)
    invoice.reload()
    client = get_client()
    client.utility.verify_payment_signature(response)
    order = client.order.fetch(response["razorpay_order_id"])
    payment = client.payment.fetch(response["razorpay_payment_id"])
    if order.get("notes", {}).get("invoice") != invoice.name or payment["order_id"] != order["id"]:
        raise frappe.PermissionError(_("Payment does not belong to this invoice"))
    if frappe.db.exists("Payment Record", {"payment_id": payment["id"], "against_invoice": invoice.name, "status": "Captured"}):
        return {"status": "already_recorded"}
    expected = minor_amount(invoice.outstanding_amount)
    if expected <= 0 or payment["status"] != "captured" or payment["amount"] != expected or payment["currency"] != invoice.currency:
        frappe.throw(_("The captured payment does not match the outstanding invoice"))
    entry = get_payment_entry("Sales Invoice", invoice.name)
    entry.reference_no = payment["id"]
    entry.reference_date = nowdate()
    entry.posting_date = nowdate()
    entry.flags.ignore_permissions = True
    entry.insert()
    entry.submit()
    frappe.get_doc({
        "doctype": "Payment Record", "order_id": order["id"], "payment_id": payment["id"],
        "signature": response["razorpay_signature"], "against_invoice": invoice.name,
        "student": invoice.student, "status": "Captured", "amount": invoice.outstanding_amount,
        "currency": invoice.currency,
    }).insert(ignore_permissions=True)
    return {"status": "recorded"}


@frappe.whitelist()
def handle_payment_failure(response: dict, against_invoice: str, billing_details: dict):
    authorized_invoice(against_invoice)
    # A client-side error is not authoritative provider or accounting state.
    return {"status": "not_recorded"}
