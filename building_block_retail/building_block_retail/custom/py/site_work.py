from frappe.utils import nowdate
import frappe
import json
from erpnext.accounts.doctype.sales_invoice.sales_invoice import get_bank_cash_account
from building_block_retail.building_block_retail.custom.py.sales_order import get_item_rate
from frappe.utils.csvutils import getlink
from frappe.utils.data import get_link_to_form
from frappe.utils import today



@frappe.whitelist()
def item_details_fetching_pavers(item_code):
    if item_code:
        doc = frappe.get_doc("Item",item_code)
        item_price = get_item_rate(item_code, check_for_uom='Square Foot')
        area_bundle= doc.bundle_per_sqr_ft
        pcs_per_bundle = doc.pavers_per_bundle or 1
        pcs_per_sqft = doc.pavers_per_sqft or 1
        return area_bundle,item_price, pcs_per_bundle, pcs_per_sqft
	
@frappe.whitelist()
def item_details_fetching_compoundwall(item_code):
    if item_code:
        doc = frappe.get_doc("Item",item_code)
        item_price = get_item_rate(item_code)
        area_bundle= doc.bundle_per_sqr_ft
        return area_bundle,item_price

def before_save(doc, action=None):
    additionalcost_total= 0
    item_details_total = 0
    job_worker_total = 0
    raw_material_total = 0
    for i in doc.additional_cost:
        additionalcost_total = additionalcost_total+ (i.amount or 0)
    doc.total = additionalcost_total
    for i in (doc.item_details or [])+(doc.item_details_compound_wall or []):
        item_details_total = item_details_total+(i.amount or 0)
    doc.total_amount=item_details_total
    for i in doc.job_worker:
        job_worker_total = job_worker_total+(i.amount or 0)
    doc.total_job_worker_cost=job_worker_total
    for i in doc.raw_material:
        raw_material_total = raw_material_total+(i.amount or 0)
    doc.total_amount_of_raw_material=raw_material_total   
    total_costing=additionalcost_total+item_details_total+raw_material_total
    doc.total_expense_amount=total_costing
    
    
    item_cost=0
    rm_cost=0
    for item in doc.item_details:
        if(item.get('warehouse')):
            bin_=frappe.get_value('Bin', {'warehouse': item.warehouse, 'item_code': item.item}, 'valuation_rate')
            item_cost+=(bin_ or 0)* (item.allocated_paver_area * frappe.db.get_value("Item", item.item, 'pavers_per_sqft') or 1)

    for item in doc.item_details_compound_wall:
        if(item.get('warehouse')):
            bin_=frappe.get_value('Bin', {'warehouse': item.warehouse, 'item_code': item.item}, 'valuation_rate')
            item_cost+=(bin_ or 0)* (item.allocated_ft * frappe.db.get_value("Item", item.item, 'pavers_per_sqft') or 1)
    
    for item in doc.raw_material:
        doc1=frappe.get_all('Item Price', {'buying':1, 'item_code': item.item}, pluck="price_list_rate")
        if(doc1):
            rm_cost+=(doc1[0] or 0)

    doc.actual_site_cost_calculation=(item_cost or 0)+(doc.total or 0)+(doc.total_job_worker_cost or 0)+ (rm_cost or 0)
    doc.site_profit = doc.total_expense_amount - doc.actual_site_cost_calculation  
    return doc

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
    doc=frappe.new_doc('Property Setter')
    doc.update({
        "doctype_or_field": "DocField",
        "doc_type":"Project",
        "field_name":"status",
        "property":"options",
        "value":"\nOpen\nLand Work Completed\nOn Process\nHold\nStock Pending at Site\nPending Qty Returned\nPart Measurement\nSite Measured\nCompleted\nCancelled"
    })
    doc.save()
    frappe.db.commit()
    
# def create_je_for_er(doc):
#     if(doc.status == 'Completed' and doc.er_employee):
#         if(not frappe.db.exists('Journal Entry', {'er_site_work':doc.name, 'docstatus':['<', 2]})):
#             income_account = frappe.get_value("Employee",doc.er_employee,"contracter_expense_account")
#             per_emp = frappe.get_value("Employee",doc.er_employee,"employee_percentage") or 0
#             hike = doc.er_total_amount * per_emp / 100
#             amt =  hike + doc.er_total_amount
#             if income_account:
#                 company = frappe.get_value('Employee', doc.er_employee, 'company')
#                 default_employee_expenses_account = frappe.get_cached_value("Company", company, "default_employee_expenses_account")
#                 def_cost_center = frappe.get_cached_value("Company", company, "cost_center")
#                 branch = frappe.get_value('Accounting Dimension Detail',{'company':company}, 'default_dimension')
#                 if default_employee_expenses_account:
#                     new_journal=frappe.get_doc({
#                         "doctype":"Journal Entry",
#                         "company":company,
#                         "posting_date":today(),
#                         "er_site_work":doc.name,
#                         "cost_center": def_cost_center,
#                         "branch":branch,
#                         "accounts":[
#                             {
#                                 "account":default_employee_expenses_account,
#                                 "credit_in_account_currency":amt,
#                                 "cost_center": def_cost_center,
#                                 "branch":branch
#                             },
#                             {
#                                 "account":income_account,
#                                 "debit_in_account_currency":amt,
#                                 "cost_center": def_cost_center,
#                                 "branch":branch
#                             },
#                         ],
#                     })
#                     new_journal.insert(ignore_mandatory=True)
#                     new_journal.submit()
#                 else:
#                     linkto = get_link_to_form("Company", company)
#                     frappe.throw(
#                         ("Enter Default Employee Expenses Account in company => {}.").format(
#                             frappe.bold(linkto)
#                         )
#                     )
#             else:
#                 linkto = get_link_to_form("Employee", doc.er_employee)
#                 frappe.throw(
#                     ("Enter Salary Account for Contractor in {}.").format(
#                         frappe.bold(linkto)
#                     )
#                 )
def validate(self,event):
    # create_je_for_er(self)
    if not self.is_new():
        validate_status(self)
        close_pending_sales_orders(self)
    validate_jw_qty(self)
    self.total_completed_qty = 0
    for i in self.finalised_job_worker_details:
        self.total_completed_qty += i.sqft_allocated
    if(self.name not in frappe.get_all('Project', pluck="name")):
        return
    amount=0
    total_amount=0
    add_cost=[]
    mode=''
    for row in self.additional_cost:
        if(row.description=="Site Advance"):
            child_name=row.name
            amount=row.amount or 0
            total_amount+=amount
            mode=row.mode_of_payment
            row.amount=0
            add_cost.append(row)
            if(amount):
                mode_of_payment = frappe.get_doc("Mode of Payment",mode).accounts
                for i in mode_of_payment:
                    if(i.company==self.company):
                        acc_paid_to=i.default_account
                        break
                try:
                    if(acc_paid_to):pass
                except:
                    frappe.throw(("Please set Company and Default account for ({0}) mode of payment").format(mode))
                
                
                doc=frappe.new_doc('Payment Entry')
                doc.update({
                    'company': self.company,
                    'source_exchange_rate': 1,
                    'payment_type': 'Receive',
                    'posting_date': nowdate(),
                    'mode_of_payment': mode,
                    'party_type': 'Customer',
                    'party': row.customer if(self.is_multi_customer) else self.customer,
                    'paid_amount': amount,
                    'paid_to': get_bank_cash_account(mode, self.company).get('account'),
                    'project': self.name,
                    'received_amount': amount,
                    'target_exchange_rate': 1,
                    'paid_to_account_currency': frappe.db.get_value('Account',acc_paid_to,'account_currency')
                })
                doc.insert()
                doc.submit()
                if(row.name and event=='after_insert'):
                    frappe.db.set_value("Additional Costs", row.name, 'amount', 0)
        else:
            add_cost.append(row)
    if(event=='after_insert'):
        frappe.db.set_value("Project", self.name, 'total_advance_amount', (self.total_advance_amount or 0)+ (total_amount or 0))
    if(event=='validate'):
        self.update({
            'additional_cost': add_cost,
            'total_advance_amount': (self.total_advance_amount or 0)+ (total_amount or 0)
        })
        
def validate_jw_qty(self):
    delivered_item={}
    for row in self.delivery_detail:
        if(row.item not  in delivered_item):
            delivered_item[row.item]=0
        # sqft=((row.delivered_bundle or 0)*float(frappe.get_value('Item', row.item, 'bundle_per_sqr_ft') or 0))+((row.delivered_pieces or 0)*float(frappe.get_value('Item', row.item, 'pavers_per_sqft') or 0))
        # item_doc=frappe.get_doc('Item', row.item, 'uoms')
        # conv_factor=[conv.conversion_factor for conv in item_doc.uoms if(conv.uom==item_doc.sales_uom)]
        # if(not sqft and not conv_factor):
        #     frappe.throw('Please enter Sales UOM for an item: '+ frappe.bold(getlink('Item', row.item)))
        # stock_qty=(row.delivered_stock_qty or 0) *(conv_factor[0] if(conv_factor) else 0)

        delivered_item[row.item]+= row.delivered_stock_qty / (frappe.get_value('Item', row.item, 'pavers_per_sqft') or 1)
    jw_items={}
    for row in self.job_worker:
        if(row.item not  in jw_items):
            jw_items[row.item]=0
        jw_items[row.item]+=float(row.sqft_allocated or 0)
    wrong_items=[]
    for item in jw_items:
        if((jw_items.get(item) or 0)>(delivered_item.get(item) or 0)):
            wrong_items.append(frappe.bold(item))
    if(wrong_items):
        frappe.throw(f"{self.name} Job Worker completed qty cannot be greater than Delivered Qty for the following items "+' '.join(wrong_items))


def set_status(document, event):
    try:
        doc=document
        if(document.doctype in ["Sales Order", "Sales Invoice", "Delivery Note"]):
            if(document.get("site_work")):
                doc=frappe.get_doc("Project", document.site_work)
        if(not doc.get("doctype")=="Project"):
            return
        linked_dn = frappe.get_all("Delivery Note", filters={'docstatus':1, 'site_work':doc.name}, pluck="name")
        dn_items = frappe.db.sql(f"""
                Select 
                    dni.item_code, dni.stock_qty
                From
                    `tabDelivery Note` dn
                    left outer join `tabDelivery Note Item` dni
                    on dni.parent = dn.name
                where
                    dn.docstatus = 1 AND
                    dn.site_work = "{doc.name}"       
            """, as_dict=1)

        inv_items = frappe.db.sql(f"""
            Select 
                sii.item_code, sii.stock_qty
            From
                `tabSales Invoice` si
                left outer join `tabSales Invoice Item` sii
                on sii.parent = si.name
            where
                si.docstatus = 1 AND
                si.site_work = "{doc.name}"       
        """, as_dict=1)

        delivered_items = {}
        for i in dn_items:
            if(i.item_code in delivered_items):
                delivered_items[i.item_code] += i.stock_qty
            else:
                delivered_items[i.item_code] = i.stock_qty

        invoiced_items = {}
        for i in inv_items:
            if(i.item_code in invoiced_items):
                invoiced_items[i.item_code] += i.stock_qty
            else:
                invoiced_items[i.item_code] = i.stock_qty
        

        total_delivered_qty = sum(delivered_items.values())
        total_invoiced_qty = sum(invoiced_items.values())
        if(total_delivered_qty):
            invoiced_percent = (total_invoiced_qty/total_delivered_qty)*100
            frappe.db.set_value("Project", doc.name, 'invoiced', invoiced_percent, update_modified=False)
        

        paid_amount = frappe.db.get_value("Payment Entry", {'docstatus':1, 'site_work':doc.name}, "sum(paid_amount)")
        outstanding_amt = frappe.db.get_value("Delivery Note", {'docstatus':1, 'site_work':doc.name}, "sum(rounded_total)")
        if(paid_amount and outstanding_amt):
            # outstanding_percent = (outstanding_amt/invoiced_amt)*100
            paid_percent = paid_amount/(outstanding_amt or 1) * 100
            frappe.db.set_value("Project", doc.name, 'payment', paid_percent, update_modified=False)
        
        required_area = sum([i.required_area for i in doc.item_details])
        jw_completed = sum([i.sqft_allocated for i in doc.job_worker])
        finalized_completed = sum([i.sqft_allocated for i in doc.finalised_job_worker_details])
        if len(doc.finalised_job_worker_details):
            frappe.db.set_value("Project", doc.name, 'completed', finalized_completed/required_area*100, update_modified=False)
        elif(jw_completed):
            frappe.db.set_value("Project", doc.name, 'completed', jw_completed/required_area*100, update_modified=False)

    except Exception as e:
        msg = f"Doc:\n{frappe.as_json(document)}\n\nEvent: {event}\n\nException:\n{e}\n\nTraceback:\n{frappe.get_traceback()}"
        frappe.log_error(title="Site Work Update Error", message=msg)


def validate_status(doc):
    old_status = frappe.get_value("Project", doc.name, "status")
    if old_status == "Completed" and doc.status != old_status:
        frappe.throw(f"Not allowed to change status from {old_status} to {doc.status}")

def close_pending_sales_orders(doc):
    from erpnext.selling.doctype.sales_order.sales_order import update_status
    if doc.status == "Completed":
        linked_so = frappe.get_all("Sales Order", filters={"docstatus":1, "site_work":doc.name, "status":["not in", ["Completed", "Closed"]]}, pluck="name")
        for i in linked_so:
            update_status("Closed", i)
