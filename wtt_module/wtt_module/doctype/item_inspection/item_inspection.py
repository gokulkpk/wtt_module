# Copyright (c) 2021, wtt_custom and contributors
# For license information, please see license.txt

# import frappe

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import cstr, cint, flt, comma_or, getdate, nowdate, formatdate, format_time, get_link_to_form
from erpnext.stock.doctype.quality_inspection_template.quality_inspection_template import get_template_details
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cstr, cint, flt, comma_or, getdate, nowdate, formatdate, format_time

class ItemInspection(Document):
	def on_submit(self):
		frappe.db.sql("UPDATE `tabPurchase Receipt` SET `total_qty`='"+str(self.total_qty)+"',`total`='"+str(self.total)+"',`base_total`='"+str(self.total)+"',`net_total`='"+str(self.total)+"' WHERE `name`='" +self.receipt_series+"'")
		for item in self.get("items"):
			for val in frappe.db.sql("SELECT return_qty FROM `tabPurchase Receipt Item` WHERE parent='"+self.receipt_series+"' and `item_code`='" +item.item_code+"'"):
				if(val[0]==0):
					if(item.ins_status == "Accepted"):
						if(item.qty==item.acc_qty):
							rej=item.qty-item.acc_qty
							frappe.db.sql("UPDATE `tabPurchase Receipt Item` SET `accepted_qty`='"+str(item.acc_qty)+"',`rejected_qty`='"+str(rej)+"',`warehouse`='"+str(item.s_warehouse)+"',`return_qty`='"+str(item.acc_qty)+"',`quality_status`='Accepted',`amount`='"+str(item.amount)+"' WHERE `parent`='" +self.receipt_series+"' AND `item_code`='" +item.item_code+"'")
						else:
							rej=item.qty-item.acc_qty
							frappe.db.sql("UPDATE `tabPurchase Receipt Item` SET `accepted_qty`='"+str(item.acc_qty)+"',`rejected_qty`='"+str(rej)+"',`warehouse`='"+str(item.s_warehouse)+"',`rejected_warehouse`='"+str(item.s_warehouse)+"',`return_qty`='"+str(item.acc_qty)+"',`quality_status`='Accepted',`amount`='"+str(item.amount)+"' WHERE `parent`='" +self.receipt_series+"' AND `item_code`='" +item.item_code+"'")

					else:	
						frappe.db.sql("UPDATE `tabPurchase Receipt Item` SET `accepted_qty`='"+str(0.00)+"',`rejected_qty`='"+str(item.qty)+"',`rejected_warehouse`='"+str(item.s_warehouse)+"',`warehouse`='',`return_qty`='"+str(item.qty)+"',`quality_status`='Rejected',`amount`='"+str(item.amount)+"' WHERE `parent`='" +self.receipt_series+"' AND `item_code`='" +item.item_code+"'")
				else:
					if(item.ins_status == "Accepted"):
						ret=val[0]+item.acc_qty
						rej=item.stock_qty-ret
						frappe.db.sql("UPDATE `tabPurchase Receipt Item` SET `accepted_qty`='"+str(ret)+"',`rejected_qty`='"+str(rej)+"',`warehouse`='"+str(item.s_warehouse)+"',`return_qty`='"+str(ret)+"',`quality_status`='Accepted',`amount`='"+str(item.amount)+"' WHERE `parent`='" +self.receipt_series+"' AND `item_code`='" +item.item_code+"'")
					else:	
						frappe.db.sql("UPDATE `tabPurchase Receipt Item` SET `accepted_qty`='"+str(0.00)+"',`rejected_qty`='"+str(item.qty)+"',`rejected_warehouse`='"+str(item.s_warehouse)+"',`warehouse`='',`return_qty`='"+str(item.qty)+"',`quality_status`='Rejected',`amount`='"+str(item.amount)+"' WHERE `parent`='" +self.receipt_series+"' AND `item_code`='" +item.item_code+"'")
		d=frappe.new_doc("Stock Entry")
		d.stock_entry_type='Material Receipt'
		d.company='W.t.t technology Services India Pvt Ltd'
		d.material_series=self.material_series
		d.to_warehouse=self.s_warehouse
		for item in self.get("items"):
			if(item.ins_status == "Accepted"):
				d.append('items',{
					'item_code':item.item_code,
					'inspection_status':'Accepted',
					'qty':item.acc_qty,
					'basic_rate':item.rate,
					'basic_amount':item.amount,
					't_warehouse':self.s_warehouse
					})
		d.submit()
		frappe.db.sql("UPDATE `tabMaterial Request` SET `overall_status`='Receipted' WHERE name='" +self.material_series+"'")
		for item in self.get("items"):
			if(item.ins_status == "Accepted"):
				frappe.db.sql("UPDATE `tabMaterial Request Item` SET `item_status`='Receipted',`stock_accepted`='"+str(item.qty)+"' WHERE `parent`='" +self.material_series+"' AND `item_code`='" +item.item_code+"'")
			else:
				frappe.db.sql("UPDATE `tabMaterial Request Item` SET `item_status`='Not Receipted',`stock_accepted`='"+str(0.00)+"' WHERE `parent`='" +self.material_series+"' AND `item_code`='" +item.item_code+"'")
		return d
@frappe.whitelist()
def make_quality_inspection(source_name, target_doc=None):
	def postprocess(source, doc):
		doc.inspected_by = frappe.session.user
		doc.get_quality_inspection_template()

	doc = get_mapped_doc("BOM", source_name, {
		'BOM': {
			"doctype": "Quality Inspection",
			"validation": {
				"docstatus": ["=", 1]
			},
			"field_map": {
				"name": "bom_no",
				"item": "item_code",
				"stock_uom": "uom",
				"stock_qty": "qty"
			},
		}
	}, target_doc, postprocess)
	return doc

@frappe.whitelist()
def make_quality(source_name, target_doc=None):
	doc = get_mapped_doc("Quality Inspection", source_name, {
		"Quality Inspection": {
			"doctype": "Stock Entry",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Quality Inspection Item": {
			"doctype": "Stock Entry Detail",
			"field_map": {
				"stock_qty": "transfer_qty",
				"batch_no": "batch_no",
				"rate":"basic_rate",
				"acc_qty":"qty"
			},
			"condition": lambda doc: doc.ins_status=="Accepted"
		}
	}, target_doc)
	return doc

	
