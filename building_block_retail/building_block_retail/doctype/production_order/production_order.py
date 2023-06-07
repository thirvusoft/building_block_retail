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
	@frappe.whitelist()
	def refresh_works(self):
		self.save()
	def validate(self):
		self.get_todo()
		self.update_item_wise_production_qty()
		self.calculate_total_in_item_wise_prod()
	
	def calculate_total_in_item_wise_prod(self):
		rows_to_remove = []
		for i in self.item_wise_production_qty:
			i.qty = ((i.get("urgent_priority") or 0) + (i.get("high_priority") or 0) + 
					(i.get("low_priority") or 0) - (i.get('qty_to_update_in_work_order') or 0))
			if(i.qty < 0):
				i.qty = 0
			if(not i.qty and not i.qty_to_update_in_work_order):
				rows_to_remove.append(i)
		for i in rows_to_remove:self.item_wise_production_qty.remove(i)
	def reload_doc(self):
		frappe.publish_realtime('reload_doc')
	def update_item_wise_production_qty(self):
		tot_qty = {}
		have_pending_qty_to_update_in_wo = {i.item_code:i for i in self.item_wise_production_qty}
		for i in self.production_order_details:
			if i.item_code not in tot_qty:
				tot_qty[i.item_code] = {
					'qty_to_produce': i.qty_to_produced,
					'color': i.color,
					frappe.scrub(i.priority): i.qty_to_produced
				}
			else:
				if(frappe.scrub(i.priority) in tot_qty[i.item_code]):
					tot_qty[i.item_code][frappe.scrub(i.priority)] += i.qty_to_produced
				else:
					tot_qty[i.item_code][frappe.scrub(i.priority)] = i.qty_to_produced
		
		item_wise_production_qty = {i.item_code:i for i in self.item_wise_production_qty}
		self.item_wise_production_qty = []
		
		for item_code, item_details in tot_qty.items():
			qty_to_produce = item_details['qty_to_produce']
			color = item_details['color']
			if(item_code in item_wise_production_qty):
				row = item_wise_production_qty[item_code]
				row.urgent_priority = item_details.get("urgent_priority") or 0
				row.high_priority = item_details.get("high_priority") or 0
				row.low_priority = item_details.get("low_priority") or 0

				## Reduce Qty to Update in WorkOrder from Total Production Qty of that Item
				# if(row.get("urgent_priority")):
				# 	row.urgent_priority -= row.qty_to_update_in_work_order or 0
				# elif(row.get("high_priority")):
				# 	row.high_priority -= row.qty_to_update_in_work_order or 0
				# elif(row.get("low_priority")):
				# 	row.low_priority -= row.qty_to_update_in_work_order or 0

				self.append('item_wise_production_qty', row.as_dict())
			else:
				self.append('item_wise_production_qty', dict(
					item_code = item_code,
					urgent_priority = item_details.get("urgent_priority") or 0,
					high_priority = item_details.get("high_priority") or 0,
					low_priority = item_details.get("low_priority") or 0,
					color=color
				))

		for i in have_pending_qty_to_update_in_wo:
			if(i not in [j.item_code for j in self.item_wise_production_qty]):	
				row = have_pending_qty_to_update_in_wo[i]
				if(i in tot_qty):
					row.urgent_priority = tot_qty[i].get("urgent_priority") or 0
					row.high_priority = tot_qty[i].get("high_priority") or 0
					row.low_priority = tot_qty[i].get("low_priority") or 0
				else:
					row.urgent_priority = 0
					row.high_priority = 0
					row.low_priority = 0
				self.append("item_wise_production_qty", row.as_dict())
		idx=1
		for i in self.item_wise_production_qty:
			i.idx = idx
			idx += 1

	def get_todo(self):
		self.works = []
		job_cards = frappe.get_all("Job Card", filters={'docstatus':['!=', 2], 'production_order':self.name}, fields=['name', 'total_completed_qty', 'docstatus'])
		jc_names = [i['name'] for i in job_cards]
		stock_entry = frappe.get_all("Stock Entry", filters={'docstatus':['!=', 2], 'ts_job_card':['in', jc_names]}, fields=['docstatus', 'name', 'ts_job_card'])
		se_created_jcs = [i['ts_job_card'] for i in stock_entry]
		se_not_created_jcs = [i for i in jc_names if i not in se_created_jcs]
		not_submitted_se = [i['name'] for i in stock_entry if(i['docstatus'] == 0)]

		for i in se_not_created_jcs:
			self.append('works', {'docname':i, 'description':f"""Need to Create Stock Entry/Submit Job Card {frappe.bold(get_link_to_form("Job Card", i))}"""})
		for i in not_submitted_se:
			self.append('works', {'docname':i, 'description':f"""Need to Submit Stock Entry {frappe.bold(get_link_to_form("Stock Entry", i))}"""})
		for i in self.item_wise_production_qty:
			if(i.qty_to_update_in_work_order and i.qty_to_update_in_work_order > 0):
				self.append('works', {'docname':i.item_code, 'description':f"""Need to Update Work Order for Item: {frappe.bold(get_link_to_form("Item", i.item_code))} - Qty: {frappe.bold(i.qty_to_update_in_work_order)}."""})
			
		
	@frappe.whitelist()
	def make_job_card(self, employee, workstation):
		if not self.today_produced_items:
			frappe.throw('Enter Today Produced Items with Qty')
		self.validate_excess_qty_with_its_jobcard()
		self.validate_excess_qty()
		items = {}
		exc_shrt = {}
		exc_shrt_jc_map = {}
		for i in self.today_produced_items:
			if(not i.produced_qty):
				continue
			if(i.produced_qty < 0):
				frappe.throw(f"""<p><b>{frappe.get_meta("Production Order").get_field("today_produced_items").label}</b></p>Row#{i.idx}: Produced Qty Must be Positive""")
			wo = frappe.db.get_value('Production Order Item', {'item_code':i.item_code, 'parent':self.name}, 'work_order')
			if(not wo):
				frappe.throw(f"""Item {frappe.bold(i.item_code)} is not mentioned in {frappe.bold("Production Order Details")} table.""")
			if(i.item_code not in items):
				items[i.item_code] = {"qty":i.produced_qty, "posting_date":i.date}
				exc_shrt[i.item_code] = {"excess_qty":i.get("excess_qty") or 0, "shortage_qty":i.get("shortage_qty") or 0}
			else:
				items[i.item_code]["qty"] += i.produced_qty
				exc_shrt[i.item_code]["excess_qty"] += i.get("excess_qty") or 0
				exc_shrt[i.item_code]["shortage_qty"] +=  i.get("shortage_qty") or 0

			for j in self.excess_and_shortage:
				exc_shrt_jc_map[j.item_code] = j.from_job_card
			if(i.excess_qty or i.shortage_qty):
				comp_qty = frappe.db.get_value("Job Card Time Log", {"parent":exc_shrt_jc_map[i.item_code]}, "final_qty")
				if(not comp_qty):
					comp_qty = frappe.db.get_value("Job Card Time Log", {"parent":exc_shrt_jc_map[i.item_code]}, "completed_qty")

				if(comp_qty-(i.get('excess_qty') or 0) + (i.get('shortage_qty') or 0) <= 0):
					frappe.throw(f"""Job Card: <b>{get_link_to_form("Job Card", exc_shrt_jc_map[i.item_code])}</b> will have 
					{comp_qty-(i.get('excess_qty') or 0) + (i.get('shortage_qty') or 0)} Qty for Salary. It should be Greater than 0.""")


				if(i.excess_qty):
					frappe.db.set_value("Job Card Time Log", {"parent":exc_shrt_jc_map[i.item_code]}, "final_qty", comp_qty-j.excess_qty)
				if(i.shortage_qty):
					frappe.db.set_value("Job Card Time Log", {"parent":exc_shrt_jc_map[i.item_code]}, "final_qty", comp_qty+j.shortage_qty)
				if(i.shortage_qty or j.excess_qty):
					frappe.db.set_value("Job Card Time Log", {"parent":exc_shrt_jc_map[i.item_code]}, "mistaken_data", 1)
			for j in self.excess_and_shortage:
				if(i.item_code == j.item_code):
					j.excess_qty -= (i.excess_qty or 0)
					j.shortage_qty -= (i.shortage_qty or 0)

		company = erpnext.get_default_company(frappe.session.user)
		jc_links = []
		self.validate_excess_and_shortage_qty(exc_shrt, items)
		for i in items:
			default_bom = get_default_bom(i)
			bom = frappe.get_doc("BOM", default_bom)
			if(not default_bom):
				frappe.throw(f"""{frappe.bold("Default BOM")} not forund for Item {frappe.bold(i)}""")
			job_card = frappe.new_doc('Job Card')
			final_qty = items[i]["qty"] - exc_shrt[i]['excess_qty'] + exc_shrt[i]['shortage_qty']
			job_card.update({	
				'production_order':self.name,
				'bom_no': default_bom,
				'company': company,
				'posting_date': items[i]["posting_date"],
				'production_item':i,
				'for_quantity':items[i]["qty"],
				'total_completed_qty':items[i]["qty"],	
				'qty_to_manufacture': items[i]["qty"],
				'operation': bom.operations[0].operation if len(bom.operations) else '',
				'workstation': workstation,
				'operation_row_number':1,
				'time_logs':[{	
					'employee':employee, 
					'completed_qty': final_qty, 
					"excess_qty":exc_shrt[i]['excess_qty'], 
					"shortage_qty":exc_shrt[i]['shortage_qty'], "final_qty":items[i]["qty"], 
					"mistaken_from":exc_shrt_jc_map.get(i) if(exc_shrt[i]['excess_qty'] or exc_shrt[i]['shortage_qty']) else None
						}]
			})
			job_card.flags.ignore_validate = True
			job_card.flags.ignore_mandatory = True
			job_card.save()
			for i in job_card.time_logs:
				if(i.mistaken_from):
					frappe.db.set_value("Job Card Time Log", {"parent":i.mistaken_from}, "excess_qty_moved_to", job_card.name)
			jc_links.append(get_link_to_form("Job Card", job_card.name))
		self.today_produced_items = []
		self.save()
		return ", ".join(jc_links)
	
	def validate_excess_and_shortage_qty(self, exc_shrt, prod_items):
		for i in exc_shrt:
			if(prod_items.get(i)):
				to_stock = prod_items[i]['qty'] - exc_shrt[i]['excess_qty'] - exc_shrt[i]['shortage_qty']
				if(to_stock <= 0):
					frappe.throw(f"""<p>Produced Qty({prod_items[i]['qty']}) - Excess Qty({exc_shrt[i]['excess_qty']}) = <b>{to_stock}</b></p>
									<p><b>Stock Qty({to_stock}) Must be Greater than 0.</b></p>""")

	def validate_excess_qty_with_its_jobcard(self):
		excess = {}
		for i in self.excess_and_shortage:
			if(i.item_code not in excess):
				excess[i.item_code] = {i.from_job_card:{"excess_qty":i.get("excess_qty") or 0, "shortage_qty":i.get("shortage_qty") or 0}}
			else:
				if(i.from_job_card in excess[i.item_code]):
					excess[i.item_code][i.from_job_card]["excess_qty"] += (i.get("excess_qty") or 0)
					excess[i.item_code][i.from_job_card]["shortage_qty"] += (i.get("shortage_qty") or 0)
				else:
					excess[i.item_code][i.from_job_card] = {"excess_qty": (i.get("excess_qty") or 0)}
					excess[i.item_code][i.from_job_card] = {"shortage_qty": (i.get("shortage_qty") or 0)}
		for items in excess:
			for jc in excess[items]:
				if(excess[items][jc]['excess_qty']):
					salary_qty = frappe.db.get_value("Job Card Time Log", {'parent':jc}, "final_qty")
					if(salary_qty < excess[items][jc]['excess_qty']):
						frappe.throw(f"""<p>In Excess Items Table</p>Row#{i.idx}: Existing Qty for Salary: {salary_qty}. But You enter {excess[items][jc]['excess_qty']} qty as Excess.""")

	def validate_excess_qty(self):
		excess = {}
		for i in self.excess_and_shortage:
			if(i.item_code not in excess):
				excess[i.item_code] = {"excess_qty":i.get("excess_qty") or 0, "shortage_qty":i.get("shortage_qty") or 0}
			else:
				excess[i.item_code]["excess_qty"] += (i.get("excess_qty") or 0)
				excess[i.item_code]["shortage_qty"] += (i.get("shortage_qty") or 0)
		for i in self.today_produced_items:
			if i.item_code in excess:
				if(i.excess_qty and i.excess_qty > excess[i.item_code]["excess_qty"]):
					frappe.throw(f"""<p>In <b>{frappe.get_meta("Production Order").get_field("today_produced_items").label}</b> table</p>
									<p>Row#{i.idx}: Excess Qty Exceeds for Item <b>{i.item_code}</b></p>
									<p>Mentioned Qty: {excess[i.item_code]["excess_qty"]}</p>
									<p>But Taken Qty: {i.excess_qty}</p>""")
				if(i.shortage_qty and i.shortage_qty > excess[i.item_code]["shortage_qty"]):
					frappe.throw(f"""<p>In <b>{frappe.get_meta("Production Order").get_field("today_produced_items").label}</b> table</p>
									<p>Row#{i.idx}: Shortage Qty Exceeds for Item <b>{i.item_code}</b></p>""")
	@frappe.whitelist()
	def update_work_order(self):
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
		if(qty):
			work_order = frappe.get_doc("Work Order", wo)
			work_order.append("produced_quantity", {"date": today(), "qty_produced": qty, "production_order": self.name})
			work_order.save()

	def update_work_order_mapped_qty(self, item, qty, work_order):
		self.reload()
		for i in self.item_wise_production_qty:
			if(i.item_code == item):
				i.qty_to_update_in_work_order -= qty

		rows_to_remove = []	
		for i in self.production_order_details:
			if(i.item_code == item and i.work_order == work_order):
				i.today_produced_qty = 0
				i.qty_to_produced -= qty
				if(i.qty_to_produced <= 0):
					rows_to_remove.append(i)
		for i in rows_to_remove:
			self.production_order_details.remove(i)
		idx=1
		for i in self.production_order_details:
			i.idx = idx
			idx += 1
		self.save()
		self.reload_doc()
		return