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
        
def on_submit(doc, action=None):
    update_production_order(doc, action)
    # update_material_shift_for_curing(doc)
    update_job_card_after_curing(doc)

def on_cancel(doc, event=None):
    update_curing_process_on_cancel(doc)

def update_curing_process_on_cancel(doc):
    update_job_card_on_cancel(doc)
    # update_material_shift_on_cancel(doc)

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

# def update_material_shift_for_curing(doc, event=None):
#     if not doc.to_curing:
#         return
#     material_shift = frappe.db.exists("Material Shifting", {"item_code":doc.production_item, "docstatus":["!=", 2]})
#     ms_doc=None
#     if material_shift:
#         ms_doc = frappe.get_doc("Material Shifting", material_shift)
#     else:
#         ms_doc = frappe.new_doc("Material Shifting")
#         ms_doc.update({
#             "item_code":doc.production_item
#         })
#     job_card = frappe.get_doc("Job Card", doc.ts_job_card)
#     actual_produced_qty = sum([i.final_qty for i in job_card.time_logs])
#     ms_doc.append("curing_in_process", {
#         "production_date":doc.posting_date,
#         "produced_qty":actual_produced_qty,
#         "from_stock_entry":doc.name,
#         "from_job_card":doc.ts_job_card,
#         "pending_qty":actual_produced_qty,
#     })
#     ms_doc.flags.ignore_mandatory=True
#     ms_doc.save(ignore_permissions=True)

def update_job_card_after_curing(doc, event=None):
    if(doc.curing_completed):
        for i in doc.items:
            if i.get("from_job_card"):
                curing_completed_qty = frappe.get_value("Job Card", i.from_job_card, "curing_completed_qty") or 0
                for_qty = sum(frappe.get_all("Job Card Time Log", {"parent": i.from_job_card}, pluck="final_qty")) or 0
                curing_completed_qty += i.qty
                curing_completed_percent = curing_completed_qty/for_qty * 100

                frappe.db.set_value("Job Card", i.from_job_card, "curing_completed_qty", curing_completed_qty)
                frappe.db.set_value("Job Card", i.from_job_card, "curing_percent", curing_completed_percent)

def update_job_card_on_cancel(doc):
    if(doc.curing_completed):
        for i in doc.items:
            if i.get("from_job_card"):
                curing_completed_qty = frappe.get_value("Job Card", i.from_job_card, "curing_completed_qty") or 0
                for_qty = frappe.get_value("Job Card", i.from_job_card, "for_quantity") or 0
                curing_completed_qty -= i.qty
                curing_completed_percent = curing_completed_qty/for_qty * 100

                frappe.db.set_value("Job Card", i.from_job_card, "curing_completed_qty", curing_completed_qty)
                frappe.db.set_value("Job Card", i.from_job_card, "curing_percent", curing_completed_percent)

# def update_material_shift_on_cancel(doc):
#     if(doc.curing_completed and doc.material_shifting):
#         for i in doc.items:
#             rows_to_remove = []
#             material_shift = frappe.get_doc("Material Shifting", doc.material_shifting)
#             if i.get("from_job_card"):
#                 prod_se = frappe.db.get_value("Stock Entry", {"ts_job_card":i.from_job_card, "docstatus":1}, "name")
#                 prod_se_doc = frappe.get_doc("Stock Entry", prod_se)
#                 if (idx:=[k.idx-1 for k in material_shift.curing_in_process if k.from_job_card == i.from_job_card]):
#                     material_shift.curing_in_process[idx[0]].update({
#                         "production_date":prod_se_doc.posting_date,
#                         "produced_qty":prod_se_doc.fg_completed_qty,
#                         "from_stock_entry":prod_se_doc.name,
#                         "from_job_card":prod_se_doc.ts_job_card,
#                         "pending_qty":i.qty + material_shift.curing_in_process[idx[0]].pending_qty,
#                     })
#                 else:
#                     material_shift.append("curing_in_process", {
#                         "production_date":prod_se_doc.posting_date,
#                         "produced_qty":prod_se_doc.fg_completed_qty,
#                         "from_stock_entry":prod_se_doc.name,
#                         "from_job_card":prod_se_doc.ts_job_card,
#                         "pending_qty":i.qty,
#                     })
                
#                 if bundled_item:=frappe.db.exists("Bundled Items", i.bundled_items_id):
#                     bundled_item_idx = frappe.get_value("Bundled Items", bundled_item, "idx")
#                     bundled_item_doc = material_shift.bundled_items[bundled_item_idx-1]
#                     material_shift.remove(bundled_item_doc)
#                     material_shift.set_idx("bundled_items")

#                 material_shift.save()