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
            frappe.throw(_("Work-in-Progress Warehouse is required before Submit"))
        if not self.fg_warehouse:
            frappe.throw(_("For Warehouse is required before Submit"))

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