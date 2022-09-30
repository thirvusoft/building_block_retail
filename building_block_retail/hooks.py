from re import M
from . import __version__ as app_version

app_name = "building_block_retail"
app_title = "Building Block Retail"
app_publisher = "Thirvusoft"
app_description = "Building Block Retail"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "thivusoft@gmail.com"
app_license = "MIT"
# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/building_block_retail/css/building_block_retail.css"
# app_include_js = "/assets/building_block_retail/js/building_block_retail.js"

# include js, css files in header of web template
# web_include_css = "/assets/building_block_retail/css/building_block_retail.css"
# web_include_js = "/assets/building_block_retail/js/building_block_retail.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "building_block_retail/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
doctype_list_js = {"Project" : "/building_block_retail/custom/js/sw_quick_entry.js",}
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

# before_install = "building_block_retail.install.before_install"
after_install = "building_block_retail.building_block_retail.function_calling.function_calling"
before_install = "building_block_retail.building_block_retail.custom.py.warehouse.create_scrap_warehouse"

# Uninstallation
# ------------

# before_uninstall = "building_block_retail.uninstall.before_uninstall"
# after_uninstall = "building_block_retail.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "building_block_retail.notifications.get_notification_config"

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
	"Payroll Entry":"building_block_retail.building_block_retail.custom.py.payroll_entry.JobWorker",
	"Opening Invoice Creation Tool":"building_block_retail.building_block_retail.custom.py.opening_invoice.OpeningInvoice",
	"Work Order":"building_block_retail.building_block_retail.custom.py.work_order.TSWorkOrder"
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
    "Item Price":{
		'validate': 'building_block_retail.building_block_retail.custom.py.item_price.validate'	
	},
    "Quotation" :{
		"before_validate": 'building_block_retail.building_block_retail.custom.py.purchase_invoice.remove_tax_percent_from_description',
		"validate" : "building_block_retail.building_block_retail.custom.py.quotation.workflow_quotation",
		"on_submit" : "building_block_retail.building_block_retail.custom.py.quotation.quotation_whatsapp"	
	},
	"Driver":{
		"validate":"building_block_retail.building_block_retail.custom.py.driver.validate_phone"
	},
	"Project":{
		"autoname":"building_block_retail.building_block_retail.custom.py.site_work.autoname",
		"before_save":"building_block_retail.building_block_retail.custom.py.site_work.before_save",
		"validate":"building_block_retail.building_block_retail.custom.py.site_work.validate",
		"after_insert":"building_block_retail.building_block_retail.custom.py.site_work.validate"
	},
	"Sales Order":{
     	"before_validate":'building_block_retail.building_block_retail.custom.py.purchase_invoice.remove_tax_percent_from_description',
        "validate" : 'building_block_retail.building_block_retail.custom.py.sales_order.add_price_list',
		"on_cancel":"building_block_retail.building_block_retail.custom.py.sales_order.remove_project_fields"
	},
	"Delivery Note":{
		"before_validate":["building_block_retail.building_block_retail.custom.py.delivery_note.update_customer",
                     	'building_block_retail.building_block_retail.custom.py.purchase_invoice.remove_tax_percent_from_description'],
		"on_submit":[
					"building_block_retail.building_block_retail.custom.py.delivery_note.update_qty_sitework",
					"building_block_retail.building_block_retail.custom.py.delivery_note.update_return_qty_sitework",
					"building_block_retail.building_block_retail.custom.py.delivery_note.delivery_note_whatsapp"
					],
		"on_cancel":[
					"building_block_retail.building_block_retail.custom.py.delivery_note.reduce_qty_sitework",
					"building_block_retail.building_block_retail.custom.py.delivery_note.reduce_return_qty_sitework"
					 ],
		"validate":["building_block_retail.building_block_retail.custom.py.delivery_note.validate",
					
					],
		"on_change":["building_block_retail.building_block_retail.custom.py.delivery_note.odometer_validate"],
  		"on_update":"building_block_retail.building_block_retail.custom.py.vehicle_log.vehicle_log_creation"
	},
	"Sales Invoice":{
    	"before_validate":["building_block_retail.building_block_retail.custom.py.sales_invoice.update_customer", 
                        'building_block_retail.building_block_retail.custom.py.purchase_invoice.remove_tax_percent_from_description'],
    	"on_submit":[
					"building_block_retail.building_block_retail.custom.py.delivery_note.update_qty_sitework",
					"building_block_retail.building_block_retail.custom.py.delivery_note.update_return_qty_sitework",
					],
		"on_cancel":[
					"building_block_retail.building_block_retail.custom.py.delivery_note.reduce_qty_sitework",
					"building_block_retail.building_block_retail.custom.py.delivery_note.reduce_return_qty_sitework"
					 ]
  	},
	"Vehicle":{
        "validate":["building_block_retail.building_block_retail.custom.py.vehicle.reference_date",
					]
    },
	"Job Card":{
		'before_submit': "building_block_retail.building_block_retail.utils.manufacturing.job_card.job_card.before_submit",
	},
	"Work Order":{
        "before_submit":"building_block_retail.building_block_retail.custom.py.work_order.before_save",
    },
    "Stock Entry":{
        "before_submit":"building_block_retail.building_block_retail.custom.py.stock_entry.before_validate",
        "on_submit":"building_block_retail.building_block_retail.custom.py.stock_entry.after_submit"
    },
    'Salary Slip':{
		'validate': 'building_block_retail.building_block_retail.custom.py.salary_slip.salary_slip_add_gross_pay',
		'on_submit':['building_block_retail.building_block_retail.custom.py.salary_slip.employee_update',
					 'building_block_retail.building_block_retail.custom.py.salary_slip.create_journal_entry'],
		'on_cancel': ['building_block_retail.building_block_retail.custom.py.salary_slip.on_cancel']
	},
    'Purchase Invoice':{
		'before_validate': 'building_block_retail.building_block_retail.custom.py.purchase_invoice.remove_tax_percent_from_description'
	},
    'Purchase Order':{
		'before_validate': 'building_block_retail.building_block_retail.custom.py.purchase_invoice.remove_tax_percent_from_description'
	},
    'Purchase Receipt':{
		'before_validate': 'building_block_retail.building_block_retail.custom.py.purchase_invoice.remove_tax_percent_from_description'
	},
    "Vehicle Log":{
		"on_update_after_submit": "building_block_retail.building_block_retail.custom.py.vehicle_log.onsubmit",
		"on_submit": ["building_block_retail.building_block_retail.custom.py.vehicle_log.onsubmit",
					  "building_block_retail.building_block_retail.custom.py.vehicle_log.update_transport_cost",
					  "building_block_retail.building_block_retail.custom.py.vehicle_log.vehicle_log_draft"],
		"on_cancel":["building_block_retail.building_block_retail.custom.py.vehicle_log.onsubmit",
					 "building_block_retail.building_block_retail.custom.py.vehicle_log.update_transport_cost"],
		"validate": "building_block_retail.building_block_retail.custom.py.vehicle_log.validate"
	},
    'BOM': {
		'validate':"building_block_retail.building_block_retail.custom.py.bom.validate"
	},
    'Employee Advance':{
		'on_submit':  'building_block_retail.building_block_retail.custom.py.employee_advance.after_insert'
	},
	'Payroll Entry':{
		'validate':'building_block_retail.building_block_retail.custom.py.payroll_entry.validate'
	},
	'Workstation' : {
		'validate': 'building_block_retail.building_block_retail.custom.py.workstation.cal_per_hour'
	}
}
after_migrate=["building_block_retail.building_block_retail.custom.py.site_work.create_status"]
doctype_js = {
				"Item" : "/building_block_retail/custom/js/item.js",
				"Payment Entry" : "/building_block_retail/custom/js/payment_entry.js",
				"Project": "/building_block_retail/custom/js/site_work.js",
				"Sales Order": [
								"/building_block_retail/custom/js/site_work.js",
								"/building_block_retail/custom/js/sales_order.js",
								],
				"Vehicle":"/building_block_retail/custom/js/vehicle.js",
				"Purchase Receipt":"/building_block_retail/custom/js/purchase_receipt.js",
				"Purchase Order": "/building_block_retail/custom/js/purchase_order.js",
				"Delivery Note": "/building_block_retail/custom/js/delivery_note.js",
				"Sales Invoice": "/building_block_retail/custom/js/sales_invoice.js",
				"Vehicle Log":"/building_block_retail/custom/js/vehicle_log.js",
				"Job Card": "/building_block_retail/custom/js/job_card.js",
				"Quotation":"/building_block_retail/custom/js/quotation.js",
    			"Work Order":"/building_block_retail/custom/js/work_order.js",
    			"Company":"/building_block_retail/custom/js/company.js",
				"Payroll Entry": "/building_block_retail/custom/js/payroll_entry.js",
				"Employee": "/building_block_retail/custom/js/employee.js",
				"Supplier": "/building_block_retail/custom/js/supplier.js",
				"Salary Slip": "/building_block_retail/custom/js/salary_slip.js" ,
				
                "Purchase Invoice":"/building_block_retail/custom/js/purchase_invoice.js"
			 }
# doctype_list_js = {"Work Order": "/building_block_retail/custom/js/work_order.js",}
# Scheduled Tasks
# ---------------

scheduler_events = {
	# "all": [
	# 	"building_block_retail.tasks.all"
	# ],
	# "daily": [
	# 	"building_block_retail.tasks.daily"
	# ],
	# "hourly": [
	# 	"building_block_retail.tasks.hourly"
	# ],
	# "weekly": [
	# 	"building_block_retail.tasks.weekly"
	# ]
	"monthly": [
		"building_block_retail.building_block_retail.custom.py.note.email_notify"
	]
}

# Testing
# -------

# before_tests = "building_block_retail.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	"erpnext.erpnext.payroll.doctype.payroll_entry.payroll_entry.make_payment_entry": "building_block_retail.building_block_retail.utils.hr.journel_entry.journel_entry.make_payment_entry",
	'erpnext.payroll.doctype.payroll_entry.payroll_entry.get_start_end_dates': 'building_block_retail.building_block_retail.custom.py.salary_slip.get_start_end_dates',
	'erpnext.payroll.doctype.payroll_entry.payroll_entry.submit_salary_slips_for_employees': 'building_block_retail.building_block_retail.custom.py.salary_slip.submit_salary_slips_for_employees',
	'erpnext.manufacturing.doctype.bom.bom.make_variant_bom' : 'building_block_retail.building_block_retail.custom.py.bom.make_variant_bom'
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "building_block_retail.task.get_dashboard_data"
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
# 	"building_block_retail.auth.validate"
# ]

# Translation
# --------------------------------

# Make link fields search translated document names for these DocTypes
# Recommended only for DocTypes which have limited documents with untranslated names
# For example: Role, Gender, etc.
# translated_search_doctypes = []