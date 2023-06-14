from dataclasses import fields
from operator import index
import frappe 
from frappe.utils.data import get_link_to_form


def validate(doc,action):
    if doc.from_bom == 1 and doc.stock_entry_type == "Manufacture" and doc.ts_job_card:
        item = frappe.get_value("Job Card", doc.ts_job_card, 'production_item')
        qty = frappe.get_value("Job Card", doc.ts_job_card, 'total_completed_qty')
        manufacturing_cost = frappe.get_value("Item", item, "employee_rate")
        expenses_included_in_valuation = frappe.get_cached_value("Company", doc.company, "expenses_included_in_valuation")
        if(not manufacturing_cost):
            link = get_link_to_form('Item', doc.production_item)
            frappe.throw(f"Manufacturing expense for <b>{doc.production_item} is 0</b>. Please set Employee Rate field > 0 in <b>{link}</b>.")
        expenses = doc.additional_costs or []
        doc.additional_costs = []
        for i in expenses:
            if not i.auto_added_row:
                doc.append('additional_costs', i)
        doc.append('additional_costs', dict(
                expense_account = expenses_included_in_valuation, amount = manufacturing_cost*qty, base_amount = manufacturing_cost*qty, 
                description = "Employee Cost", auto_added_row = 1
            ))
        doc.distribute_additional_costs()
        doc.update_valuation_rate()
        


def update_production_order(doc, event=None):
    if(doc.production_order and doc.bom_no):
        pro_doc = frappe.get_doc("Production Order", doc.production_order)
        fg_item = frappe.db.get_value("BOM", doc.bom_no, "item")
        for i in pro_doc.item_wise_production_qty:
            if( i.item_code == fg_item and event == "on_submit"):
                i.qty_to_update_in_work_order += doc.fg_completed_qty
                if(i.get("urgent_priority")):
                    i.urgent_priority -= doc.fg_completed_qty
                elif(i.get("high_priority")):
                    i.high_priority -= doc.fg_completed_qty
                elif(i.get("low_priority")):
                    i.low_priority -= doc.fg_completed_qty
        pro_doc.save()