from building_block_retail.building_block_retail.custom.py.defaults import create_defaults
from building_block_retail.building_block_retail.utils.Inventory.item import item_customization
from building_block_retail.building_block_retail.utils.accounting.accounts.accounts import account_customization
from building_block_retail.building_block_retail.utils.accounting.accounts.bank_account import bank_account_customization
from building_block_retail.building_block_retail.utils.buying.purchase_invoice import purchase_invoice
# from building_block_retail.building_block_retail.utils.buying.purchase_invoice import purchase_invoice
from building_block_retail.building_block_retail.utils.buying.purchase_order import purchase_order
from building_block_retail.building_block_retail.utils.buying.purchase_receipt import purchase_receipt
from building_block_retail.building_block_retail.utils.buying.request_for_quotation import request_for_quotation
from building_block_retail.building_block_retail.utils.buying.supplier_quotation import supplier_quotation
from building_block_retail.building_block_retail.utils.crm.customer.customer import customer_customizations
from building_block_retail.building_block_retail.utils.crm.lead.lead import lead_customisation
from building_block_retail.building_block_retail.utils.crm.customer.address import address_customization
from building_block_retail.building_block_retail.utils.hr.employee.employee import employee_customisations
from building_block_retail.building_block_retail.utils.hr.employee.employee_advance import employee_advance_customization
from building_block_retail.building_block_retail.utils.hr.payroll.payroll_entry import payroll_entry_customization
from building_block_retail.building_block_retail.utils.hr.role.roles import create_role
from building_block_retail.building_block_retail.utils.hr.salary_slip.salary_slip import create_salary_custom_field
from building_block_retail.building_block_retail.utils.manufacturing.job_card.job_card import create_job_card_custom_fields
from building_block_retail.building_block_retail.utils.selling.sales_invoice.sales_invoice_custom_fields import sales_invoice_customization
from building_block_retail.building_block_retail.utils.projects.site_work.site_work import customize_field
from building_block_retail.building_block_retail.utils.projects.site_work.site_work import site_doc_name 
from building_block_retail.building_block_retail.utils.selling.delivery_note.delivery_note import delivery_note_customization
from building_block_retail.building_block_retail.create_docs import create_docs
from building_block_retail.building_block_retail.utils.selling.sales_order.sales_order import sales_order_customization
from building_block_retail.building_block_retail.utils.hr.vehicle.vehicle import vehicle_customization
from building_block_retail.building_block_retail.utils.crm.quotation.quotation import quotation_customization
from building_block_retail.building_block_retail.custom.py.workflow import workflow_document_creation
from building_block_retail.building_block_retail.utils.manufacturing.work_order.work_order import work_order_custom
from building_block_retail.building_block_retail.utils.manufacturing.workstation.workstation import workstation_custom
from building_block_retail.building_block_retail.utils.accounting.journal_entry.journal_entry import journal_entry_customization
from building_block_retail.building_block_retail.utils.accounting.company.company import company_customization
from building_block_retail.building_block_retail.utils.stock.stock_entry.stock_entry import stock_entry_custom
from building_block_retail.building_block_retail.utils.Inventory.item_custom import item_Customization
from building_block_retail.building_block_retail.utils.property_setter import create_property_setter
from building_block_retail.building_block_retail.utils.hr.driver.driver import driver_customization
from building_block_retail.building_block_retail.utils.hr.vehicle_log.vehicle_log import vehicle_log_customization
from building_block_retail.building_block_retail.utils.selling.sales_order.sales_order import item_details_pavers_customization
def function_calling():
    payroll_entry_customization()
    create_defaults()
    create_salary_custom_field()
    employee_advance_customization()
    address_customization()
    create_docs()
    customer_customizations()
    lead_customisation()
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
    employee_customisations()
    work_order_custom()
    create_role()
    create_job_card_custom_fields()
    workstation_custom()
    journal_entry_customization()
    company_customization()
    account_customization()
    stock_entry_custom()
    create_property_setter()
    driver_customization()
    vehicle_log_customization()
    bank_account_customization()
    item_details_pavers_customization()
    
def execute():
    function_calling()
