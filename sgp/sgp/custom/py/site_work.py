from audioop import add
from frappe.utils import nowdate
import frappe
import json
from erpnext.accounts.doctype.sales_invoice.sales_invoice import get_bank_cash_account

@frappe.whitelist()
def item_details_fetching_pavers(item_code):
    if item_code:
        doc = frappe.get_doc("Item",item_code)
        item_price = doc.standard_rate
        area_bundle= doc.bundle_per_sqr_ft
        return area_bundle,item_price
	
@frappe.whitelist()
def item_details_fetching_compoundwall(item_code):
    if item_code:
        doc = frappe.get_doc("Item",item_code)
        item_price = doc.standard_rate
        area_bundle= doc.bundle_per_sqr_ft
        return area_bundle,item_price

def before_save(doc, action):
    additionalcost_total= 0
    item_details_total = 0
    job_worker_total = 0
    raw_material_total = 0
    for i in doc.additional_cost:
        additionalcost_total = additionalcost_total+ (i.amount or 0)
    doc.total = additionalcost_total
    for i in doc.item_details:
        item_details_total = item_details_total+(i.amount or 0)
    doc.total_amount=item_details_total
    for i in doc.job_worker:
        job_worker_total = job_worker_total+(i.amount or 0)
    doc.total_job_worker_cost=job_worker_total
    for i in doc.raw_material:
        raw_material_total = raw_material_total+(i.amount or 0)
    doc.total_amount_of_raw_material=raw_material_total   
    total_costing=additionalcost_total+item_details_total+job_worker_total+raw_material_total
    doc.total_expense_amount=total_costing
		

@frappe.whitelist()
def add_total_amount(items):
    if items:
        return sum([i['amount'] for i in json.loads(items)])


def autoname(self, event):
    if(not self.project_name):
        frappe.throw('Please Enter Site Work Name')
    else:
        name= self.project_name
    if(not self.is_multi_customer and not self.customer):
        frappe.throw("Please Enter Customer's Name")
    elif(not self.is_multi_customer):
        name+= '-' + self.customer
        self.project_name+='-'+self.customer
    if(name):
        self.name=name
    else:
        pass
        
def create_status():
    print('Creating Property Setter for Site Work Status')
    doc=frappe.new_doc('Property Setter')
    doc.update({
        "doctype_or_field": "DocField",
        "doc_type":"Project",
        "field_name":"status",
        "property":"options",
        "value":"\nOpen\nCompleted\nCancelled\nStock Pending at Site"
    })
    doc.save()
    frappe.db.commit()
    

def validate(self,event):
    amount=0
    add_cost=[]
    for row in self.additional_cost:
        if(row.description=="Site Advance"):
            amount=row.amount
            row.amount=0
            add_cost.append(row)
        else:
            add_cost.append(row)
    if(amount!=0 and self.is_multi_customer==0):
        mode_of_payment = frappe.get_doc("Mode of Payment",'Cash').accounts
        for i in mode_of_payment:
            if(i.company==self.company):
                acc_paid_to=i.default_account
                break
        try:
            if(acc_paid_to):pass
        except:
            frappe.throw(("Please set Company and Default account for ({0}) mode of payment").format('Cash'))
        
        
        doc=frappe.new_doc('Payment Entry')
        doc.update({
            'company': self.company,
            'source_exchange_rate': 1,
            'payment_type': 'Receive',
            'posting_date': nowdate(),
            'mode_of_payment': 'Cash',
            'party_type': 'Customer',
            'party': self.customer,
            'paid_amount': amount,
            'paid_to': get_bank_cash_account('Cash', self.company).get('account'),
            'project': self.name,
            'received_amount': amount,
            'target_exchange_rate': 1,
            'paid_to_account_currency': frappe.db.get_value('Account',acc_paid_to,'account_currency')
        })
        doc.insert()
        doc.submit()
        self.update({
            'additional_cost': add_cost,
            'total_advance_amount': (self.total_advance_amount or 0)+amount
        })
            