from erpnext.stock.doctype.item.item import get_item_details
from frappe.model.mapper import get_mapped_doc
import frappe

def validate(doc, event):
    for i in doc.operations:
        if(i.time_in_mins == 0):i.time_in_mins=10
        
        
@frappe.whitelist()
def make_variant_bom(source_name, bom_no, item, variant_items, target_doc=None):
	from erpnext.manufacturing.doctype.work_order.work_order import add_variant_item

	def postprocess(source, doc):
		doc.item = item
		doc.quantity = source.quantity

		item_data = get_item_details(item)
		doc.update(
			{
				"item_name": item_data.item_name,
				"description": item_data.description,
				"uom": item_data.stock_uom,
				"allow_alternative_item": item_data.allow_alternative_item,
			}
		)

		add_variant_item(variant_items, doc, source_name)

	doc = get_mapped_doc(
		"BOM",
		source_name,
		{
			"BOM": {"doctype": "BOM", "validation": {"docstatus": ["=", 1]}},
			"BOM Item": {
				"doctype": "BOM Item",
				# stop get_mapped_doc copying parent bom_no to children
				"field_no_map": ["bom_no"],
				"condition": lambda doc: doc.has_variants == 0,
			},
		},
		target_doc,
		postprocess,
	)

	return doc