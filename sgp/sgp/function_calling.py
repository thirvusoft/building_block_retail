from sgp.sgp.utils.Inventory.item import item_customization
from sgp.sgp.utils.buying.purchase_invoice import purchase_invoice
# from sgp.sgp.utils.buying.purchase_invoice import purchase_invoice
from sgp.sgp.utils.buying.purchase_order import purchase_order
from sgp.sgp.utils.buying.purchase_receipt import purchase_receipt
from sgp.sgp.utils.buying.request_for_quotation import request_for_quotation
from sgp.sgp.utils.buying.supplier_quotation import supplier_quotation


def function_calling():
    purchase_invoice()
    purchase_order()
    purchase_receipt()
    request_for_quotation()
    supplier_quotation()
    item_customization()
  

