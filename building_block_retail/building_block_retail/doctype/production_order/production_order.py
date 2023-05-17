# Copyright (c) 2023, Thirvusoft and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document

class ProductionOrder(Document):
	def validate(self):
		tot_qty = {}
		for i in self.production_order_details:
			if i.item_code not in tot_qty:
				tot_qty[i.item_code] = {
					'qty_to_produce': i.qty_to_produced,
					'color': i.color
				}
			else:
				tot_qty[i.item_code]['qty_to_produce'] += i.qty_to_produced
		self.item_wise_production_qty = []
		for item_code, item_details in tot_qty.items():
			qty_to_produce = item_details['qty_to_produce']
			color = item_details['color']
			self.append('item_wise_production_qty', dict(
				item_code = item_code,
				qty=qty_to_produce,
				color=color
			))
