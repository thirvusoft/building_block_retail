import frappe 

def set_value_in_jobcard_after_stock_entry(self, event):
    if(self.work_order):
        jc_qty = frappe.db.get_value("Job Card", {'work_order':self.work_order}, "total_completed_qty")
        se_qty = sum(frappe.db.get_all("Stock Entry", filters={'work_order':self.work_order,'docstatus':1},pluck="fg_completed_qty"))
        if(jc_qty == se_qty):
            frappe.db.set_value("Job Card", {'work_order':self.work_order}, "se_created", 1)
            frappe.db.commit()