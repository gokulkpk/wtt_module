from __future__ import unicode_literals
import frappe
import json

from frappe.utils import cstr, flt, getdate, new_line_sep, nowdate, add_days, get_link_to_form
from frappe import msgprint, _
from frappe.model.mapper import get_mapped_doc
from erpnext.stock.stock_balance import update_bin_qty, get_indented_qty
from erpnext.controllers.buying_controller import BuyingController
from erpnext.manufacturing.doctype.work_order.work_order import get_item_details
from erpnext.buying.utils import check_on_hold_or_closed_status, validate_for_items
from erpnext.stock.doctype.item.item import get_item_defaults

class MaterialRequest(BuyingController):
	def validate(self):
		super(MaterialRequest, self).validate()

		self.validate_schedule_date()
		self.check_for_on_hold_or_closed_status('Sales Order', 'sales_order')
		self.validate_uom_is_integer("uom", "qty")

		if not self.status:
			self.status = "Draft"

		from erpnext.controllers.status_updater import validate_status
		validate_status(self.status,
			["Draft", "Submitted", "Stopped", "Cancelled", "Pending",
			"Partially Ordered", "Ordered", "Issued", "Transferred", "Received"])

		validate_for_items(self)

		self.set_title()
		# self.validate_qty_against_so()
		# NOTE: Since Item BOM and FG quantities are combined, using current data, it cannot be validated
		# Though the creation of Material Request from a Production Plan can be rethought to fix this

	def set_title(self):
		'''Set title as comma separated list of items'''
		if not self.title:
			items = ', '.join([d.item_name for d in self.items][:3])
			self.title = _('{1}').format(self.material_request_type, items)[:100]



@frappe.whitelist()
def make_request(source_name, target_doc=None):
	def postprocess(source, target):
		target.material_request_type="Material Issue"
		target.schedule_date=target.transaction_date
		for i in target.get("items"):
			i.schedule_date=target.transaction_date
	doc = get_mapped_doc("Material Request", source_name, {
		"Material Request": {
			"doctype": "Material Request",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Material Request Item": {
			"doctype": "Material Request Item",
			"field_map": {
				"stock_accepted": "qty"
			},
			"condition": lambda doc: doc.item_status=="Receipted"
		}
	}, target_doc,postprocess)
	return doc

@frappe.whitelist()
def make_request_for_quotation(source_name, target_doc=None):
	doclist = get_mapped_doc("Material Request", source_name, 	{
		"Material Request": {
			"doctype": "Request for Quotation",
			"validation": {
				"docstatus": ["=", 1],
				"material_request_type": ["=", "Purchase"]
			},
			"field_map": {
				"name": "material_series"
			}
		},
		"Material Request Item": {
			"doctype": "Request for Quotation Item",
			"field_map": [
				["name", "material_request_item"],
				["parent", "material_request"],
				["uom", "uom"]
			]
		}
	}, target_doc)

	return doclist