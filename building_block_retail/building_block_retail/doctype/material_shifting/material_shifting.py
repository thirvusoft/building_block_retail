# Copyright (c) 2023, Thirvusoft and contributors
# For license information, please see license.txt

import frappe
import json
import erpnext
from frappe.model.document import Document
from frappe.utils import nowdate, get_link_to_form

class MaterialShifting(Document):
	def prepend(self, key, value={}):
		self.__dict__[key] = self.__dict__[key][::-1]
		self.append(key, value)
		self.__dict__[key] = self.__dict__[key][::-1]
		self.set_idx(key)
	
	def set_idx(self, key):
		idx=1
		for i in self.__dict__[key]:
			i.idx = idx
			idx += 1

	def validate(self):
		if len(self.bundled_items) >= 10:
			self.bundled_items = self.bundled_items[:10:]

def make_bundled_stock_entry(material_shift, bundled_data, job_card_data):
	stock_entry = frappe.new_doc("Stock Entry")
	se_items = []
	bundle_salary_per_piece = frappe.db.get_value("Item", material_shift.item_code, "bundling_cost")
	if not bundle_salary_per_piece:
		frappe.throw(f"""Missing Bundle cost in Item <b>{get_link_to_form("Item", material_shift.item_code)}</b> """)
	for i in job_card_data:
		to_warehouse = frappe.db.get_value("Stock Entry", {"docstatus":1, "ts_job_card":i}, "to_warehouse")
		se_items.append({
			"s_warehouse":to_warehouse,
			"t_warehouse":bundled_data.get("bundled_warehouse"),
			"item_code":material_shift.item_code,
			"qty":job_card_data[i],
			"conversion_factor":1,
			"from_job_card":i,
			"bundled_items_id":material_shift.bundled_items[0].name,
			"pcs_per_bundle": bundled_data.get("pcs_per_bundle"),
			"no_of_bundle": bundled_data.get("no_of_bundle"),
			"bundling_cost": bundle_salary_per_piece * job_card_data[i]
		})
	stock_entry.update({
		'posting_date': bundled_data.get("bundled_date"),
		'set_posting_time':1,
		'curing_completed':1,
		'material_shifting':material_shift.name,
		'purpose': "Material Transfer",
		'company': erpnext.get_default_company(),
		"items":se_items,
		"bundling_employee":bundled_data.get("bundling_employee"),
		"salary_per_piece": bundle_salary_per_piece,
		"total_bundles":bundled_data.get("no_of_bundle"),
		"total_pcs":bundled_data.get("no_of_pcs"),
		"total_salary": (bundled_data.get("no_of_pcs") or 0) * bundle_salary_per_piece,
	})

	stock_entry.set_stock_entry_type()
	stock_entry.save()
	stock_entry.submit()


@frappe.whitelist()
def update_curing_stock(docname, values, selected_rows_id):
	if isinstance(values, str):
		values = json.loads(values)
	if isinstance(selected_rows_id, str):
		selected_rows_id = json.loads(selected_rows_id)

	
	doc = frappe.get_doc("Material Shifting", docname)
	selected_production_qty = values["stock_qty"]
	rows_to_add = []
	job_card_data={}

	for i in doc.curing_in_process:
		if i.name in selected_rows_id and selected_production_qty:
			if selected_production_qty >= i.pending_qty:
				selected_production_qty -= i.pending_qty
				job_card_data[i.from_job_card] = i.pending_qty
			else:
				i.pending_qty -= selected_production_qty
				job_card_data[i.from_job_card] = selected_production_qty
				rows_to_add.append(i.as_dict())
				selected_production_qty=0
		else:
			rows_to_add.append(i.as_dict())
	
	idx = 1

	doc.curing_in_process = []

	for i in rows_to_add:
		del i["name"]
		i["idx"] = idx
		doc.append("curing_in_process", i)
		idx+=1

	bundled_data = {
		"bundled_date" : nowdate(),
		"pcs_per_bundle" : values.get("pcs_per_bundle"),
		"no_of_pcs" : values.get("no_of_pieces"),
		"no_of_bundle" : values.get("no_of_bundle"),
		"bundled_qty" : values.get("stock_qty"),
		"job_card_data": json.dumps(job_card_data),
		"bundled_warehouse": values.get("fg_warehouse") or doc.get("warehouse")
	}
	doc.prepend("bundled_items", bundled_data)

	doc.save()
	bundled_data.update(values)
	make_bundled_stock_entry(material_shift= doc, bundled_data= bundled_data, job_card_data= job_card_data)