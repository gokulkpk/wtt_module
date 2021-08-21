from __future__ import unicode_literals
import frappe, json
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.utils import get_url, cint
from frappe.utils.user import get_user_fullname
from frappe.utils.print_format import download_pdf
from frappe.desk.form.load import get_attachments
from frappe.core.doctype.communication.email import make
from erpnext.accounts.party import get_party_account_currency, get_party_details
from erpnext.stock.doctype.material_request.material_request import set_missing_values
from erpnext.controllers.buying_controller import BuyingController
from erpnext.buying.utils import validate_for_items

from six import string_types

STANDARD_USERS = ("Guest", "Administrator")

@frappe.whitelist()
def create_supplier_quotation(doc):
	if isinstance(doc, string_types):
		doc = json.loads(doc)
		sq_doc = frappe.get_doc({
			"doctype": "Supplier Quotation",
			"supplier": doc.get('supplier'),
			"terms": doc.get("terms"),
			"request_for_quotation":doc.get('name'),
			"company": doc.get("company"),
			"freight_amount":doc.get("fre"),
			"p_and_f":doc.get("p_f"),
			"price_basis":doc.get("price_basis"),
			"delivary_time":doc.get("d_t"),
			"payment_terms":doc.get("p_t"),
			"warranty":doc.get("war"),
			"supplier_freight":doc.get("fre"),
			"supplier_p_and_f":doc.get("p_f"),
			"supplier_price_basis":doc.get("price_basis"),
			"supplier_delivary_time":doc.get("d_t"),
			"supplier_payment_terms":doc.get("p_t"),
			"supplier__warranty":doc.get("war"),
			"currency": doc.get('currency') or get_party_account_currency('Supplier', doc.get('supplier'), doc.get('company')),
			"buying_price_list": doc.get('buying_price_list') or frappe.db.get_value('Buying Settings', None, 'buying_price_list')
		})
		add_items(sq_doc, doc.get('supplier'), doc.get('items'))
		sq_doc.flags.ignore_permissions = True
		sq_doc.run_method("set_missing_values")
		sq_doc.save()
		frappe.msgprint(_("Supplier Quotation {0} Created").format(sq_doc.name))
		return sq_doc.name

def add_items(sq_doc, supplier, items):
	for data in items:
		if data.get("qty") > 0:
			if isinstance(data, dict):
				data = frappe._dict(data)

			create_rfq_items(sq_doc, supplier, data)

def create_rfq_items(sq_doc, supplier, data):
	sq_doc.append('items', {
		"item_code": data.item_code,
		"item_name": data.item_name,
		"description": data.description,
		"qty": data.qty,
		"stock_qty":data.stock_qty,
		"rate": data.rate,
		"item_tax_template":data.gst,
		"supplier_description":data.des,
		"conversion_factor": data.conversion_factor if data.conversion_factor else None,
		"supplier_part_no": frappe.db.get_value("Item Supplier", {'parent': data.item_code, 'supplier': supplier}, "supplier_part_no"),
		"warehouse": data.warehouse or '',
		"request_for_quotation_item": data.name,
		"request_for_quotation": data.parent,
		"material_request":data.material_request,
		"uom_rate":data.uom_rate
	})
	sq_doc.append('supplier_data',{
		"item_code": data.item_code,
		"item_name": data.item_name,
		"description": data.description,
		"qty": data.qty,
		"rate": data.rate,
		"item_tax_template":data.gst,
		"amount":data.amount,
		"supplier_description":data.des
	})