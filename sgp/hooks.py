from . import __version__ as app_version

app_name = "sgp"
app_title = "Sgp"
app_publisher = "ts@info.in"
app_description = "customization"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "ts@info.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/sgp/css/sgp.css"
# app_include_js = "/assets/sgp/js/sgp.js"

# include js, css files in header of web template
# web_include_css = "/assets/sgp/css/sgp.css"
# web_include_js = "/assets/sgp/js/sgp.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "sgp/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
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

# before_install = "sgp.install.before_install"
after_install = "sgp.sgp.function_calling.function_calling"
before_install = "sgp.sgp.custom.py.warehouse.create_scrap_warehouse"

# Uninstallation
# ------------

# before_uninstall = "sgp.uninstall.before_uninstall"
# after_uninstall = "sgp.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "sgp.notifications.get_notification_config"

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
	# "Salary Slip":"ganapathy_pavers.utils.py.salary_slip.CustomSalary",
	# "Payroll Entry":"ganapathy_pavers.utils.py.payroll_entry.MessExpense",
	"Opening Invoice Creation Tool":"sgp.sgp.custom.py.opening_invoice.OpeningInvoice"
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
doc_events = {
	"Driver":{
		"validate":"sgp.sgp.custom.py.driver.validate_phone"
	},
	"Project":{
		"autoname":"sgp.sgp.custom.py.site_work.autoname",
		"before_save":"sgp.sgp.custom.py.site_work.before_save",
		"validate":"sgp.sgp.custom.py.site_work.validate",
		"after_insert":"sgp.sgp.custom.py.site_work.validate"
	},
	"Sales Order":{
		"on_cancel":"sgp.sgp.custom.py.sales_order.remove_project_fields"
	},
	"Delivery Note":{
		"before_validate":"sgp.sgp.custom.py.delivery_note.update_customer",
		"on_submit":[
					"sgp.sgp.custom.py.delivery_note.update_qty_sitework",
					"sgp.sgp.custom.py.delivery_note.update_return_qty_sitework",
					],
		"on_cancel":[
					"sgp.sgp.custom.py.delivery_note.reduce_qty_sitework",
					"sgp.sgp.custom.py.delivery_note.reduce_return_qty_sitework"
					 ],
		"validate":["sgp.sgp.custom.py.delivery_note.validate",
					],
		"on_change":["sgp.sgp.custom.py.delivery_note.odometer_validate",]

	},
	# "Job Card":{
	# 	"on_submit": "sgp.sgp.custom.py.job_card.create_timesheet"
	# },
	"Sales Invoice":{
    	"before_validate":"sgp.sgp.custom.py.sales_invoice.update_customer"
  	},
	"Vehicle":{
        "validate":"sgp.sgp.custom.py.vehicle.reference_date",
    },
	"Stock Entry":{
		'on_submit': "sgp.sgp.custom.py.stock_entry.set_value_in_jobcard_after_stock_entry"
	},
	"Job Card":{
		'before_submit': "sgp.sgp.utils.manufacturing.job_card.job_card.before_submit"
	},
	"Work Order":{
        "on_change":"sgp.sgp.custom.py.work_order.before_save",
    },
    "Stock Entry":{
        "before_submit":"sgp.sgp.custom.py.stock_entry.before_validate",
    },

}
after_migrate=["sgp.sgp.custom.py.site_work.create_status"]
doctype_js = {
				"Item" : "/sgp/custom/js/item.js",
				"Payment Entry" : "/sgp/custom/js/payment_entry.js",
				"Project": "/sgp/custom/js/site_work.js",
				"Sales Order": [
								"/sgp/custom/js/site_work.js",
								"/sgp/custom/js/sales_order.js",
								],
				"Vehicle":"/sgp/custom/js/vehicle.js",
				"Purchase Receipt":"/sgp/custom/js/purchase_receipt.js",
				"Delivery Note": "/sgp/custom/js/delivery_note.js",
				"Sales Invoice": "/sgp/custom/js/sales_invoice.js",
				"Vehicle Log":"/sgp/custom/js/vehicle_log.js",
				"Job Card": "/sgp/custom/js/job_card.js",
				"Quotation":"/sgp/custom/js/quotation.js",
    			"Work Order":"/sgp/custom/js/work_order.js",
    			"Company":"/sgp/custom/js/company.js",
				"Payroll Entry": "/sgp/custom/js/payroll_entry.js",
				"Employee": "/sgp/custom/js/employee.js"
			 }
# doctype_list_js = {"Work Order": "/sgp/custom/js/work_order.js",}
# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"sgp.tasks.all"
# 	],
# 	"daily": [
# 		"sgp.tasks.daily"
# 	],
# 	"hourly": [
# 		"sgp.tasks.hourly"
# 	],
# 	"weekly": [
# 		"sgp.tasks.weekly"
# 	]
# 	"monthly": [
# 		"sgp.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "sgp.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	"erpnext.erpnext.payroll.doctype.payroll_entry.payroll_entry.make_payment_entry": "sgp.sgp.utils.hr.journel_entry.journel_entry.make_payment_entry"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "sgp.task.get_dashboard_data"
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
# 	"sgp.auth.validate"
# ]

# Translation
# --------------------------------

# Make link fields search translated document names for these DocTypes
# Recommended only for DocTypes which have limited documents with untranslated names
# For example: Role, Gender, etc.
# translated_search_doctypes = []
