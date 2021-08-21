# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np

def execute(filters=None):
    if not filters:
        return [], []
    data = []
    columns = get_columns(filters)
    data = get_data(data , filters)
    return columns, data

def get_columns(filters):
    columns=[
        {
            "label": _("Item Code"),
            "fieldtype": "Data",
            "fieldname": "item_code",
            "width": 150
        },
        {
            "label": _("Description"),
            "fieldtype": "Data",
            "fieldname": "description",
            "width": 250
        }
    ]
    val=frappe.db.sql("SELECT supplier FROM `tabSupplier Quotation` WHERE request_for_quotation=%(request_for_quotation)s and revision='Final Revision'",filters,as_dict=1)
    for i in val:
        columns.append({
            "fieldname": i.supplier+"qty",
            "label": i.supplier+" - "+"Qty",
            "fieldtype": "Float",
            "width": 100
        })
    for i in val:
        columns.append({
            "fieldname": i.supplier+"gst",
            "label": i.supplier+" - "+"Gst",
            "fieldtype": "Data",
            "width": 120
        })
    for i in val:
        columns.append({
            "fieldname": i.supplier+"rate",
            "label": i.supplier+" - "+"Price",
            "fieldtype": "Data",
            "width": 120
        })
    for i in val:
        columns.append({
            "fieldname": i.supplier+"amount",
            "label": i.supplier+" - "+"Amount",
            "fieldtype": "Link",
            "options":"Supplier Quotation",
            "width": 120
        })
    for i in val:
        columns.append({
            "fieldname": i.supplier+"description",
            "label": i.supplier+" - "+"Supplier Description",
            "fieldtype": "Data",
            "width": 250
        })
    return columns

def get_data(data, filters):
    data=[]
    to_be_compared_items = frappe.db.sql("""SELECT sq.supplier_name, sq.name, soi.item_code,soi.description,soi.qty, soi.rate, soi.amount, soi.item_tax_template,soi.supplier_description FROM `tabSupplier Quotation Item` as soi inner join `tabSupplier Quotation` as sq on sq.name = soi.parent where sq.request_for_quotation = %(request_for_quotation)s AND sq.transaction_date between %(from_date)s and %(to_date)s""",filters,as_dict = 1)
    query=frappe.db.sql("SELECT name,workflow_state,supplier_name,freight_amount,p_and_f,gst,grand_total,total,price_basis,delivary_time,payment_terms,warranty FROM `tabSupplier Quotation` WHERE request_for_quotation=%(request_for_quotation)s",filters,as_dict=1)
    items_dict = {}
    temp_list = []
    for item in to_be_compared_items:
        temp_list.append(item.item_code)
    unique_item = set(temp_list)

    for item in unique_item:
        column = {}
        for datum in to_be_compared_items:
            if item == datum.item_code:
                column['item_code'] = datum.item_code
                column['description'] = datum.description
                #column['qty'] = datum.qty
                column[datum.supplier_name + 'qty'] = datum.qty
                column[datum.supplier_name + 'gst'] = datum.item_tax_template
                column[datum.supplier_name + 'rate'] = datum.rate
                column[datum.supplier_name + 'amount'] = datum.amount
                column[datum.supplier_name + 'description'] = datum.supplier_description
        data.append(column)
    column2={}
    for item in query:
        column2['item_code'] = "Total"
        column2[item.supplier_name + 'amount'] = item.total
    column3={}
    for item in query:
        column3['item_code'] = "Freight Amount"
        column3[item.supplier_name + 'amount'] = item.freight_amount
    column4={}
    for item in query:
        column4['item_code'] = "P & F"
        column4[item.supplier_name + 'amount'] = item.p_and_f
    column5={}
    for item in query:
        column5['item_code'] = "Grand Total"
        column5[item.supplier_name + 'amount'] = item.grand_total
    column6={}
    for item in query:
        column6['item_code'] = "Price Basis"
        column6[item.supplier_name + 'amount'] = item.price_basis
    column7={}
    for item in query:
        column7['item_code'] = "Payment Terms"
        column7[item.supplier_name + 'amount'] = item.payment_terms
    column8={}
    for item in query:
        column8['item_code'] = "Warranty"
        column8[item.supplier_name + 'amount'] = item.warranty
    column9={}
    for item in query:
        column9['item_code'] = "Delivary Time"
        column9[item.supplier_name + 'amount'] = item.delivary_time
    column10={}
    for item in query:
        column10['item_code'] = "Supplier Link"
        column10[item.supplier_name + 'amount'] = item.name
    column11={}
    for item in query:
        column11['item_code'] = "Workflow status"
        column11[item.supplier_name + 'amount'] = item.workflow_state
    data.append(column2)
    data.append(column3)
    data.append(column4)
    data.append(column5)
    data.append(column6)
    data.append(column7)
    data.append(column8)
    data.append(column9)
    data.append(column10)
    data.append(column11)
    return data

'''
    pr_dict={}
    pr_list=[]
    query=frappe.db.sql("SELECT name,supplier_name FROM `tabSupplier Quotation` WHERE material_series=%(mr)s",filters,as_dict=1)
    for i in query:
        sql=frappe.db.sql("SELECT name1,value FROM `tabPo_terms` WHERE parent='"+i.name+"'",as_dict=1)
        for pr in sql:
            pr_list.append(pr.name1)
        for pr in pr_list:
            column2 ={}
            for datum in sql:
                if pr == datum.name1:
                    column2['item_code'] = datum.name1
                    column2[i.supplier_name + 'amount'] = datum.value
            data.append(column2)
    column3={}
    for item in query:
        column3['item_code'] = "Supplier Link"
        column3[item.supplier_name + 'amount'] = item.name
        data.append(column3)
    return data
'''