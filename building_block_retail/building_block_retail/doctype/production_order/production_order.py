# Copyright (c) 2023, Thirvusoft and contributors
# For license information, please see license.txt

# import frappe
import json
from frappe.model.document import Document

class ProductionOrder(Document):
	def validate(self):
		tot_qty = {}
		for i in self.production_order_details:
			if i.item_code not in tot_qty:
				tot_qty[i.item_code] = i.qty_to_produced
			else:
				tot_qty[i.item_code] += i.qty_to_produced
		self.item_wise_production_qty = []
		for m in tot_qty:
			
			self.append('item_wise_production_qty', dict(
				item_code = m,
				qty=tot_qty[m],
			))
