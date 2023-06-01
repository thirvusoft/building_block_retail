# Copyright (c) 2023, Thirvusoft and contributors
# For license information, please see license.txt

import frappe
import erpnext
import json
from frappe.model.document import Document
from erpnext.stock.get_item_details import get_default_bom
from frappe.utils.data import get_link_to_form
from frappe.utils import (
	today
)


class ProductionOrder(Document):
	def validate(self):
		self.get_todo()
		self.update_item_wise_production_qty()

	def calculate_final_qty(self):
		for i in self.today_produced_items:
			i.final_qty = (i.produced_qty or 0) - (i.excess_qty or 0) + (i.shortage_qty or 0)
	
	def reload_doc(self):
		frappe.publish_realtime('reload_doc')
	def update_item_wise_production_qty(self):
		tot_qty = {}
		for i in self.production_order_details:
			if i.item_code not in tot_qty:
				tot_qty[i.item_code] = {
					'qty_to_produce': i.qty_to_produced,
					'color': i.color
				}
			else:
				tot_qty[i.item_code]['qty_to_produce'] += i.qty_to_produced
		
		
		item_wise_production_qty = {i.item_code:i for i in self.item_wise_production_qty}
		self.item_wise_production_qty = []
		
		for item_code, item_details in tot_qty.items():
			qty_to_produce = item_details['qty_to_produce']
			color = item_details['color']
			if(item_code in item_wise_production_qty):
				row = item_wise_production_qty[item_code]
				row.qty = qty_to_produce
				self.append('item_wise_production_qty', row.as_dict())
			else:
				self.append('item_wise_production_qty', dict(
					item_code = item_code,
					qty=qty_to_produce,
					color=color
				))

	def get_todo(self):
		self.works = []
		job_cards = frappe.get_all("Job Card", filters={'docstatus':['!=', 2], 'production_order':self.name}, fields=['name', 'total_completed_qty', 'docstatus'])
		jc_names = [i['name'] for i in job_cards]
		stock_entry = frappe.get_all("Stock Entry", filters={'docstatus':['!=', 2], 'ts_job_card':['in', jc_names]}, fields=['docstatus', 'name', 'ts_job_card'])
		se_created_jcs = [i['ts_job_card'] for i in stock_entry]
		se_not_created_jcs = [i for i in jc_names if i not in se_created_jcs]
		not_submitted_se = [i['name'] for i in stock_entry if(i['docstatus'] == 0)]

		for i in se_not_created_jcs:
			self.append('works', {'docname':i, 'description':f"""Need to Submit Job Card {frappe.bold(get_link_to_form("Job Card", i))}"""})
		for i in not_submitted_se:
			self.append('works', {'docname':i, 'description':f"""Need to Submit Stock Entry {frappe.bold(get_link_to_form("Stock Entry", i))}"""})
		for i in self.item_wise_production_qty:
			if(i.qty_to_update_in_work_order and i.qty_to_update_in_work_order > 0):
				self.append('works', {'docname':i.item_code, 'description':f"""Need to Update Work Order for Item: {frappe.bold(get_link_to_form("Item", i.item_code))} - Qty: {frappe.bold(i.qty_to_update_in_work_order)}."""})
			
		
	@frappe.whitelist()
	def make_job_card(self, employee, workstation):
		if not self.today_produced_items:
			frappe.throw('Enter Today Produced Items with Qty')
		items = {}
		for i in self.today_produced_items:
			if(not i.final_qty):
				continue
			if(i.final_qty < 0):
				frappe.throw(f"""Row#{i.idx}: Final Qty Must be Positive""")
			wo = frappe.db.get_value('Production Order Item', {'item_code':i.item_code, 'parent':self.name}, 'work_order')
			if(not wo):
				frappe.throw(f"""Item {frappe.bold(i.item_code)} is not mentioned in {frappe.bold("Production Order Details")} table.""")
			if(i.item_code not in items):
				items[i.item_code] = i.final_qty
			else:
				items[i.item_code] += i.final_qty

			if(i.excess_qty or i.shortage_qty):
				for j in self.excess_and_shortage:
					if(j.item_code == i.item_code):
						j.excess_qty -= (i.excess_qty or 0)
						j.shortage_qty -= (i.shortage_qty or 0)
						continue


		company = erpnext.get_default_company(frappe.session.user)
		jc_links = []
		for i in items:
			default_bom = get_default_bom(i)
			bom = frappe.get_doc("BOM", default_bom)
			if(not default_bom):
				frappe.throw(f"""{frappe.bold("Default BOM")} not forund for Item {frappe.bold(i)}""")
			job_card = frappe.new_doc('Job Card')
			job_card.update({	
				'production_order':self.name,
				'bom_no': default_bom,
				'company': company,
				'posting_date': today(),
				'production_item':i,
				'qty_to_manufacture': items[i],
				'operation': bom.operations[0].operation if len(bom.operations) else '',
				'workstation': workstation,
				'operation_row_number':1,
				'time_logs':[{'employee':employee, 'completed_qty':items[i]}]
			})
			job_card.flags.ignore_validate = True
			job_card.flags.ignore_mandatory = True
			job_card.save()
			jc_links.append(get_link_to_form("Job Card", job_card.name))
		self.today_produced_items = []
		self.save()
		return ", ".join(jc_links)
	
	@frappe.whitelist()
	def update_work_order(self):
		if (sum([i.today_produced_qty or 0 for i in self.production_order_details]) <= 0):
			frappe.publish_realtime("no_qty_update_work_order")
			return

		max_qty_for_items = {i.item_code:i.qty_to_update_in_work_order for i in self.item_wise_production_qty}
		update_qty = {}
		for i in self.production_order_details:
			if(i.item_code in update_qty):
				update_qty[i.item_code] += i.today_produced_qty
			else:
				update_qty[i.item_code] = i.today_produced_qty
		for i in update_qty:
			if(i not in max_qty_for_items):
				frappe.throw(f"""Item {frappe.bold(i)} has no qty to update.""")
			elif( update_qty[i] > max_qty_for_items[i]):
				frappe.throw(f"""Item {frappe.bold(i)} has {max_qty_for_items[i]} Qty to update. But you try to update {update_qty[i]} Qty.""")
		
		for i in self.production_order_details:
			if(i.today_produced_qty):
				self.update_qty_in_work_order(i.work_order, i.today_produced_qty)
			self.update_work_order_mapped_qty(i.item_code, i.today_produced_qty, i.work_order)

	def update_qty_in_work_order(self, wo, qty):
		work_order = frappe.get_doc("Work Order", wo)
		work_order.append("produced_quantity", {"date": today(), "qty_produced": qty, "production_order": self.name})
		work_order.save()

	def update_work_order_mapped_qty(self, item, qty, work_order):
		self.reload()
		for i in self.item_wise_production_qty:
			if(i.item_code == item):
				frappe.errprint(qty)
				i.qty_to_update_in_work_order -= qty
				frappe.errprint(i.qty_to_update_in_work_order)

		rows_to_remove = []	
		for i in self.production_order_details:
			if(i.item_code == item and i.work_order == work_order):
				i.today_produced_qty -= qty
				frappe.errprint(i.qty_to_produced)
				i.qty_to_produced -= qty
				if(i.qty_to_produced <= 0):
					rows_to_remove.append(i)
		for i in rows_to_remove:
			self.production_order_details.remove(i)
		self.save()
		self.reload_doc()
		return