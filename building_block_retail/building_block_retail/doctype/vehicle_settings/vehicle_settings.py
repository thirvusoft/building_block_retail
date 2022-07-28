# Copyright (c) 2022, Thirvusoft and contributors
# For license information, please see license.txt

import frappe
from building_block_retail.building_block_retail.custom.py.vehicle_log import validate
from frappe.model.document import Document

class VehicleSettings(Document):
	def validate(Document):
		if Document.admin_email_id == None or Document.admin_email_id == "" or Document.fleet_manager_email_id == None or Document.fleet_manager_email_id == " ":
			frappe.throw("Set Default Admin and Fleet Manager User Id")
