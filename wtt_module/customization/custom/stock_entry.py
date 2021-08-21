import frappe
import json

@frappe.whitelist()
def make_filter(go):
	fetch = frappe.db.sql("SELECT `name` FROM `tabItem` WHERE has_variants='1' and item_group='"+go+"'")
	return fetch

@frappe.whitelist()
def make_template(val1):
	query=frappe.db.sql("SELECT DISTINCT(attribute) FROM `tabItem Variant Attribute` WHERE variant_of='"+val1+"'",as_dict=1)
	att_value = []
	for i in query:
		att_v = frappe.db.sql("SELECT DISTINCT(attribute_value) FROM `tabItem Variant Attribute` WHERE attribute='"+i.attribute+"'",as_dict=1)
		att_v = [j.attribute_value for j in att_v]
		att_value.append(att_v)
	return [query, att_value]

@frappe.whitelist()
def make_filtering(ar,ar1):
	frappe.msgprint(str(ar)+"-"+str(ar1))