# Copyright (c) 2023, Thirvusoft and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document
from frappe.utils import nowdate

class MaterialShifting(Document):
	pass

@frappe.whitelist()
def make_bundled_stock_entry(docname, values):
	if isinstance(values, str):
		values = json.loads(values)
	
	doc = frappe.get_doc("Material Shifting", docname)
	doc.append("bundled_items", {
		"bundled_date" : nowdate(),
		"pcs_per_bundle" : values.get("pcs_per_bundle"),
		"no_of_pcs" : values.get("no_of_pieces"),
		"no_of_bundle" : values.get("no_of_bundle"),
		"bundled_qty" : values.get("stock_qty"),
	})
	doc.save()