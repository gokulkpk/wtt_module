# Copyright (c) 2021, IT WTT and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document
import functools
import calendar
from datetime import date
from datetime import datetime
from frappe.model.document import Document

class SundayAttendance(Document):
	def validate(self):
		for employee in frappe.db.sql("SELECT name,employee_name,salary FROM `tabEmployee` WHERE status='Active' AND employee='WTT1199' AND branch='HEAD OFFICE'",as_dict=1):
			for i in frappe.db.sql("SELECT COUNT(employee) FROM tabAttendance WHERE attendance_date>='"+self.from_date+"' AND attendance_date<='"+self.to_date+"' AND employee='"+employee.name+"' AND status='Present'"):
				res = functools.reduce(lambda sub, ele: sub * 10 + ele, i)
				val=res/6
				go=val+1
				total=(employee.salary)/30*round(go)
				doc = frappe.new_doc("Additional Salary")
				doc.employee=employee.name
				doc.salary_component='Sundays'
				doc.payroll_date=date.today()
				doc.amount=total
				doc.submit()
				return doc
				frappe.msgprint(str(employee.name)+"-"+str(employee.employee_name)+"-"+str(total))
				#frappe.msgprint(str(employee.name)+"-"+str(employee.employee_name)+"-"+str(round(go))+"-"+str(employee.per_day_salary))
