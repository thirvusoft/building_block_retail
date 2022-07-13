from sgp.sgp.utils.Inventory.item import item_customization
from sgp.sgp.utils.buying.purchase_invoice import purchase_invoice
# from sgp.sgp.utils.buying.purchase_invoice import purchase_invoice
from sgp.sgp.utils.buying.purchase_order import purchase_order
from sgp.sgp.utils.buying.purchase_receipt import purchase_receipt
from sgp.sgp.utils.buying.request_for_quotation import request_for_quotation
from sgp.sgp.utils.buying.supplier_quotation import supplier_quotation
from sgp.sgp.utils.hr.role.roles import create_role
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
def function_calling():
    purchase_order()
    purchase_invoice()
    purchase_receipt()
    request_for_quotation()
    supplier_quotation()
    item_customization()
    sales_invoice_customization()
    customize_field()
    site_doc_name()
    delivery_note_customization()
    sales_order_customization()
    vehicle_customization()
    quotation_customization()
    workflow_document_creation()
    work_order_custom()
    create_role()
