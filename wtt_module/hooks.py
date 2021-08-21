from . import __version__ as app_version

app_name = "wtt_module"
app_title = "wtt_module"
app_publisher = "wtt_module"
app_description = "wtt_module"
app_icon = "wtt_module"
app_color = "grey"
app_email = "wtt_module"
app_license = "wtt_module"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/wtt_module/css/wtt_module.css"
# app_include_js = "/assets/wtt_module/js/wtt_module.js"

# include js, css files in header of web template
# web_include_css = "/assets/wtt_module/css/wtt_module.css"
# web_include_js = "/assets/wtt_module/js/wtt_module.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "wtt_module/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Material Request":"customization/custom/material_request.js",
	"Item Inspection":"customization/custom/item_inspection.js",
	"Request for Quotation":"customization/custom/request_for_quotation.js",
	"Supplier Quotation":"customization/custom/supplier_quotation.js",
	"Purchase Receipt":"customization/custom/purchase_receipt.js",
	"Stock Entry":"customization/custom/stock_entry.js"
}
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "wtt_module.install.before_install"
# after_install = "wtt_module.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "wtt_module.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes
override_doctype_class = {
 	"Material Request": "wtt_module.customization.custom.material_request.MaterialRequest",
 	"Purchare Receipt": "wtt_module.customization.custom.material_request.PurchaseReceipt"
}
# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"wtt_module.tasks.all"
# 	],
# 	"daily": [
# 		"wtt_module.tasks.daily"
# 	],
# 	"hourly": [
# 		"wtt_module.tasks.hourly"
# 	],
# 	"weekly": [
# 		"wtt_module.tasks.weekly"
# 	]
# 	"monthly": [
# 		"wtt_module.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "wtt_module.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "wtt_module.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "wtt_module.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"wtt_module.auth.validate"
# ]

