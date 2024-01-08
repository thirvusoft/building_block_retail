# Copyright (c) 2024, Thirvusoft and contributors
# For license information, please see license.txt

from building_block_retail import uom_conversion
import erpnext
import frappe
from frappe.model.document import Document
from frappe.utils.data import get_link_to_form

class CuringChamber(Document):
	def validate(self):
		for row in self.items:
			if ((row.to_bundle_qty or 0) + (row.today_remaining_qty or 0)) > ((row.production_qty or 0) + (row.before_remaining_qty or 0)):
				frappe.throw(msg=f"Incorrect values in row {row.idx}")
			row.damaged_qty = ((row.production_qty or 0) + (row.before_remaining_qty or 0)) - ((row.to_bundle_qty or 0) + (row.today_remaining_qty or 0))

	def validate_curing(self):
		self.validate()
		for row in self.items:
			if not row.to_bundle_qty:
				frappe.throw(f"Please enter <b>To Bundle Qty</b> in row {row.idx} or remove this row.")

			if not row.not_bundled and not row.employee:
				frappe.throw(f"Employee is required in row {row.idx}")
			
			if not row.finished_warehouse:
				frappe.throw(f"Finished Warehouse is required in row {row.idx}")
			
			if row.damaged_qty and not row.scrap_warehouse:
				frappe.throw(f"Scrap Warehouse is required in row {row.idx}")
	
	@frappe.whitelist()
	def complete_curing(self):
		if (cc:=frappe.get_all("Stock Entry", {"curing_chamber": self.name, 'docstatus': ["!=", 2]}, pluck='name')):
			frappe.throw(f"""Curing process is already completed.
				<ul>
				{"".join([f"<li><a href='/app/stock-entry/{i}'>{i}</a></li>" for i in cc])}
				</ul>""")

		self.validate_curing()
		
		item_job_cards = {}

		stock_entry = frappe.new_doc("Stock Entry")
		se_items = []
		for row in self.items:
			bundle_salary_per_piece = frappe.db.get_value("Item", row.item, "bundling_cost")
			if not bundle_salary_per_piece:
				frappe.throw(f"""Missing Bundle cost in Item <b>{get_link_to_form("Item", row.item)}</b> """)
			
			if row.item not in item_job_cards:
				before_date_items = frappe.db.get_all("Job Card", [
					['docstatus', '=', 1],
					['to_curing', '=', 1],
					['curing_percent', '<', 100],
					['production_item', '=', row.item],
					['Job Card Time Log', 'employee', '=', row.employee],
					['Job Card Time Log', 'from_time', '<', f"{self.date} 00:00:00"]
				], ['name', 'for_quantity', 'curing_completed_qty', 'target_warehouse'])

				on_date_items = frappe.db.get_all("Job Card", [
					['docstatus', '=', 1],
					['to_curing', '=', 1],
					['curing_percent', '<', 100],
					['production_item', '=', row.item],
					['Job Card Time Log', 'employee', '=', row.employee],
					['Job Card Time Log', 'from_time', 'between', [f"{self.date} 00:00:00", f"{self.date} 23:59:59"]]
				], ['name', 'for_quantity', 'curing_completed_qty', 'target_warehouse'])

				item_job_cards[row.item] = before_date_items + on_date_items

			remaining_qty = row.to_bundle_qty
			damaged_qty = row.damaged_qty
			
			job_cards = item_job_cards[row.item]

			jc_idx = 0
			while jc_idx < len(job_cards):
				job_card = job_cards[jc_idx]
				if not frappe.db.get_all("Stock Entry", {"ts_job_card": job_card.name, "docstatus": 1}):
					jc_idx += 1
					continue

				if not remaining_qty and not damaged_qty:
					break
				
				if 'qty' not in job_card:
					job_card.qty = ((job_card.for_quantity or 0) - (job_card.curing_completed_qty or 0))
				
				if not job_card.qty:
					jc_idx += 1
					continue

				if remaining_qty:
					qty = job_card.qty
					if job_card.qty > remaining_qty:
						qty = remaining_qty
						remaining_qty = 0
					else:
						remaining_qty -= job_card.qty

					job_card.qty -= qty

					if (job_card.target_warehouse == row.finished_warehouse):
						frappe.throw(f"Source and Target Warehouse <b>({row.finished_warehouse})</b> cannot be same for row {row.idx}")

					se_items.append({
						"s_warehouse": job_card.target_warehouse,
						"t_warehouse": row.finished_warehouse,
						"item_code": row.item,
						"qty": qty,
						"conversion_factor": 1,
						"from_job_card": job_card.name,
						"bundling_employee": row.employee if not row.not_bundled else '',
						"not_bundled": row.not_bundled,
						"pcs_per_bundle": uom_conversion(item=row.item, from_uom='bundle', from_qty=1, to_uom='Nos'),
						"no_of_bundle": row.to_bundle_qty / uom_conversion(item=row.item, from_uom='bundle', from_qty=1, to_uom='Nos'),
						"bundling_cost": bundle_salary_per_piece * row.to_bundle_qty
					})

				if not remaining_qty and damaged_qty:
					qty = job_card.qty
					if job_card.qty > damaged_qty:
						qty = damaged_qty
						damaged_qty = 0
					else:
						damaged_qty -= job_card.qty

					job_card.qty -= qty

					if (job_card.target_warehouse == row.finished_warehouse):
						frappe.throw(f"Source and Target Warehouse <b>({row.finished_warehouse})</b> cannot be same for row {row.idx}")
					
					se_items.append({
						"s_warehouse": job_card.target_warehouse,
						"t_warehouse": row.scrap_warehouse,
						"item_code": row.item,
						"qty": qty,
						"conversion_factor": 1,
						"from_job_card": job_card.name,
						"pcs_per_bundle": uom_conversion(item=row.item, from_uom='bundle', from_qty=1, to_uom='Nos'),
						"no_of_bundle": row.to_bundle_qty / uom_conversion(item=row.item, from_uom='bundle', from_qty=1, to_uom='Nos'),
						"is_scrap_item": 1,
						"is_process_loss": 1
					})
				
				if job_card.qty == 0:
					jc_idx += 1
				
			if (remaining_qty + damaged_qty) > 0:
				emp_name = frappe.get_value("Employee", row.employee, "employee_name")
				frappe.throw(f"Insufficient Job Cards for Item <b>{row.item}</b> Employee <b>{row.employee} {emp_name}</b>.<br>Expected Qty: {row.to_bundle_qty + row.damaged_qty}.<br>Shortage Qty: {remaining_qty + damaged_qty}")
		
		stock_entry.update({
			'posting_date': self.posting_date,
			'set_posting_time': 1,
			'curing_completed': 1,
			'curing_chamber': self.name,
			'purpose': "Material Transfer",
			'company': erpnext.get_default_company(),
			"items": se_items,
			"total_bundles": sum([(i.get("no_of_bundle") or 0) for i in se_items]),
			"total_pcs": sum([(i.get("qty") or 0) for i in se_items]),
			"total_salary": sum([(i.get("bundling_cost") or 0) for i in se_items]),
		})

		stock_entry.set_stock_entry_type()

		stock_entry.save()

		self.status = 'Completed'
		self.save()
		frappe.msgprint(f"Stock Entry Created Successfully <a href='/app/stock-entry/{stock_entry.name}'>{stock_entry.name}</a>")
		frappe.local.response['stock-entry'] = stock_entry.name

	@frappe.whitelist()
	def fetch_items(self):
		if (cc:=frappe.get_all("Stock Entry", {"curing_chamber": self.name, 'docstatus': ["!=", 2]}, pluck='name')):
			frappe.throw(f"""Curing process is already completed.
				<ul>
				{"".join([f"<li><a href='/app/stock-entry/{i}'>{i}</a></li>" for i in cc])}
				</ul>""")

		if not self.date:
			frappe.throw("Please enter the date.")

		before_date_items = frappe.db.get_all("Job Card", [
			['docstatus', '=', 1],
			['to_curing', '=', 1],
			['curing_percent', '<', 100],
			['Job Card Time Log', 'from_time', '<', f"{self.date} 00:00:00"]
		], ['name', 'production_item', 'for_quantity', 'curing_completed_qty', 'target_warehouse', '`tabJob Card Time Log`.employee'])

		on_date_items = frappe.db.get_all("Job Card", [
			['docstatus', '=', 1],
			['to_curing', '=', 1],
			['curing_percent', '<', 100],
			['Job Card Time Log', 'from_time', 'between', [f"{self.date} 00:00:00", f"{self.date} 23:59:59"]]
		], ['name', 'production_item', 'for_quantity', 'curing_completed_qty', 'target_warehouse', '`tabJob Card Time Log`.employee'])
		
		items = {}
		for item in before_date_items:
			__key = f"{item.production_item}----{item.employee}"
			if not frappe.db.get_all("Stock Entry", {"ts_job_card": item.name, "docstatus": 1}):
				continue
			
			if __key not in items:
				items[__key] = {
						"item": item.production_item,
						"before_remaining_qty": 0,
						"employee": item.employee
					}
			
			items[__key]["before_remaining_qty"] = (items[__key].get("before_remaining_qty") or 0) + ((item.get("for_quantity") or 0) - (item.get("curing_completed_qty") or 0))
		
		for item in on_date_items:
			__key = f"{item.production_item}----{item.employee}"
			if not frappe.db.get_all("Stock Entry", {"ts_job_card": item.name, "docstatus": 1}):
				continue

			if __key not in items:
				items[__key] = {
						"item": item.production_item,
						"production_qty": 0,
						"employee": item.employee
					}
			items[__key]["production_qty"] = (items[__key].get("production_qty") or 0) + ((item.get("for_quantity") or 0) - (item.get("curing_completed_qty") or 0))
		
		self.update({
			"items": list(items.values())
		})
		self.save()
		
		frappe.msgprint(msg="Items updated.", indicator='green', alert=True)
		return self
