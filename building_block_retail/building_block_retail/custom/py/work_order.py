from erpnext.manufacturing.doctype.work_order.work_order import WorkOrder
import frappe
from frappe.utils.data import get_link_to_form

def before_save(doc,action):
    item=frappe.get_doc("Item",doc.production_item)
    if(not item.employee_rate):
        link = get_link_to_form('Item', doc.production_item)
        frappe.throw(f"Manufacturing expense for <b>{doc.production_item} is 0</b>. Please set Employee Rate field > 0 in <b>{link}</b>.")
    doc.total_expanse = item.employee_rate
 
class TSWorkOrder(WorkOrder):   
    def on_submit(self):
        """Work Order on_submit Over Written Code"""
        if not self.wip_warehouse and not self.skip_transfer:
            frappe.throw(("Work-in-Progress Warehouse is required before Submit"))
        if not self.fg_warehouse:
            frappe.throw(("For Warehouse is required before Submit"))

        if self.production_plan and frappe.db.exists(
            "Production Plan Item Reference", {"parent": self.production_plan}
        ):
            self.update_work_order_qty_in_combined_so()
        else:
            self.update_work_order_qty_in_so()

        self.update_reserved_qty_for_production()
        self.update_completed_qty_in_material_request()
        self.update_planned_qty()
        self.update_ordered_qty()
        ##Prevent Auto Create Job Card
        # self.create_job_card()
        
    def validate_work_order_against_so(self):
        return
    
def production_order_creation(doc,action):
    item_doc=frappe.get_doc("Item",doc.production_item)
    if not frappe.db.exists("Production Order",item_doc.variant_of or item_doc.name):
        new_doc=frappe.new_doc("Production Order")
        # item_doc=frappe.get_doc("Item",doc.production_item)
        if(item_doc.variant_of):
            for j in item_doc.attributes:
                if j.attribute =="Colour":
                    new_doc.update({
                    "item_template":item_doc.variant_of or item_doc.name,
                    "production_order_details":[{
                    "work_order":doc.name,
                    "qty_to_produced":doc.qty,
                    "color":j.attribute_value,
                    "priority":doc.priority,
                    "item_code":doc.production_item
                    }],
                    })
                    new_doc.save()
        else:
            new_doc.update({
                    "item_template":item_doc.variant_of or item_doc.name,
                    "production_order_details":[{
                    "work_order":doc.name,
                    "qty_to_produced":doc.qty,
                    "priority":doc.priority,
                    "item_code":doc.production_item
                    }],
                    })
        new_doc.save()
    else:
        item_doc=frappe.get_doc("Item",doc.production_item)
        production_doc=frappe.get_doc("Production Order",item_doc.variant_of or doc.production_item)
        if(item_doc.variant_of):
            for j in item_doc.attributes:
                if j.attribute =="Colour":
                    production_doc.append("production_order_details",{
                        "work_order":doc.name,
                        "qty_to_produced":doc.qty,
                        "color":j.attribute_value,
                        "priority":doc.priority,
                        "item_code":doc.production_item
                    })
                    production_doc.save()
        else:
            production_doc.append( "production_order_details", {
                    "work_order":doc.name,
                    "qty_to_produced":doc.qty,
                    "priority":doc.priority,
                    "item_code":doc.production_item
                })
        production_doc.save()

def validate(doc, event):
    update_manufactured_qty(doc, event)
    update_status(doc, event)

def update_manufactured_qty(doc, event):
    doc.produced_qty = 0
    
    for i in doc.produced_quantity:
        doc.produced_qty += (i.qty_produced or 0)
    if event == "on_update_after_submit":
        frappe.db.set_value("Work Order", doc.name, "produced_qty", doc.produced_qty)
        frappe.db.set_value("Work Order Operation", {'parent': doc.name}, 'completed_qty', doc.produced_qty)

def update_status(doc, event):
    if(doc.produced_qty >= doc.qty):
        doc.status = "Completed"
    elif(doc.produced_qty  <= 0):
        doc.status = "Not Started"
    elif(doc.produced_qty < doc.qty):
        doc.status = "In Process"
    if event == "on_update_after_submit":
        frappe.db.set_value("Work Order", doc.name, "status", doc.status)


def on_change(doc, event=None):
    update_sales_order(doc)
    update_site_work(doc)

def update_sales_order(doc):
    if(doc.sales_order):
        work_orders = frappe.db.get_all("Work Order", filters={'sales_order':doc.sales_order, 'docstatus':1}, fields=["sum(qty) as qty_to_manufacture", "sum(produced_qty) as produced_qty"], group_by="sales_order")
        if(len(work_orders)):
            produced_percent = round((work_orders[0]["produced_qty"] / work_orders[0]["qty_to_manufacture"]) * 100, 2)
            frappe.db.set_value("Sales Order", doc.sales_order, "per_produced", produced_percent)

def update_site_work(doc):
    if(doc.project):
        work_orders = frappe.db.get_all("Work Order", filters={'project':doc.project, 'docstatus':1}, fields=["sum(qty) as qty_to_manufacture", "sum(produced_qty) as produced_qty"], group_by="project")
        if(len(work_orders)):
            produced_percent = round((work_orders[0]["produced_qty"] / work_orders[0]["qty_to_manufacture"]) * 100, 2)
            frappe.db.set_value("Project", doc.project, "per_produced", produced_percent)