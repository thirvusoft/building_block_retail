from sgp.sgp.custom.py.defaults import create_designation
from sgp.sgp.utils.Inventory.item import item_customization
from sgp.sgp.utils.accounting.accounts.accounts import account_customization
from sgp.sgp.utils.buying.purchase_invoice import purchase_invoice
# from sgp.sgp.utils.buying.purchase_invoice import purchase_invoice
from sgp.sgp.utils.buying.purchase_order import purchase_order
from sgp.sgp.utils.buying.purchase_receipt import purchase_receipt
from sgp.sgp.utils.buying.request_for_quotation import request_for_quotation
from sgp.sgp.utils.buying.supplier_quotation import supplier_quotation
from sgp.sgp.utils.hr.employee.employee import create_contracter_expense_account
from sgp.sgp.utils.hr.role.roles import create_role
from sgp.sgp.utils.manufacturing.job_card.job_card import create_job_card_custom_fields
from sgp.sgp.utils.selling.sales_invoice.sales_invoice_custom_fields import sales_invoice_customization
from sgp.sgp.utils.projects.site_work.site_work import customize_field
from sgp.sgp.utils.projects.site_work.site_work import site_doc_name 
from sgp.sgp.utils.selling.delivery_note.delivery_note import delivery_note_customization
from sgp.sgp.create_docs import create_docs
from sgp.sgp.utils.selling.sales_order.sales_order import sales_order_customization
from sgp.sgp.utils.hr.vehicle.vehicle import vehicle_customization
from sgp.sgp.utils.crm.quotation.quotation import quotation_customization
from sgp.sgp.custom.py.workflow import workflow_document_creation
from sgp.sgp.utils.manufacturing.work_order.work_order import work_order_custom
from sgp.sgp.utils.manufacturing.workstation.workstation import workstation_custom
from sgp.sgp.utils.accounting.journal_entry.journal_entry import journal_entry_customization
from sgp.sgp.utils.accounting.company.company import company_customization
from sgp.sgp.utils.stock.stock_entry.stock_entry import stock_entry_custom
from sgp.sgp.utils.Inventory.item_custom import item_Customization
def function_calling():
    create_docs()
    purchase_order()
    purchase_invoice()
    purchase_receipt()
    request_for_quotation()
    supplier_quotation()
    item_Customization()
    item_customization()
    sales_invoice_customization()
    customize_field()
    site_doc_name()
    delivery_note_customization()
    sales_order_customization()
    vehicle_customization()
    quotation_customization()
    workflow_document_creation()
    create_role()
    create_contracter_expense_account()
    work_order_custom()
    create_role()
    create_job_card_custom_fields()
    workstation_custom()
    journal_entry_customization()
    company_customization()
    account_customization()
    stock_entry_custom()
    create_designation()