import frappe
from erpnext.controllers.taxes_and_totals import get_itemised_tax
from erpnext.controllers.taxes_and_totals import get_itemised_taxable_amount
def update_customer(self,event):
    cus=self.customer
    for row in self.items:
        so=row.sales_order
        if(so):
            doc=frappe.get_doc('Sales Order', so)
            if(cus!=doc.customer):
                frappe.db.set(doc, "customer", cus)
def on_submit(self, event):
    if(self.site_work and self.work == 'Supply and Laying'):
        site_work = frappe.get_doc("Project", self.site_work)
        for i in self.job_worker_table:
            site_work.append('job_worker', {
                'name1':self.jobworker_name,
                'item':i.item_code,
                'sqft_allocated': i.sqft,
                'rate':i.ratesqft,
                'amount':i.ts_amount
                })
        site_work.save(ignore_permissions=True)