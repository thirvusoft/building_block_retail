import frappe
import json
from erpnext.stock.get_item_details import get_default_bom
from frappe.utils.data import flt

def update_qty_sitework(self,event):
    if(self.doctype=='Sales Invoice' and self.update_stock==0):
        return
    if(not self.is_return):
        for row in self.items:
            so=(row.against_sales_order if self.doctype=='Delivery Note' else row.sales_order)
            if(so):
                sw=frappe.get_value('Sales Order', so, 'site_work')
                if(sw):
                    item_group=frappe.get_value('Item', row.item_code, 'item_group')
                    doc=frappe.get_doc('Project', sw)
                    delivery_detail=doc.delivery_detail
                    create=1
                    for item in range(len(delivery_detail)):
                        if(row.item_code==delivery_detail[item].item and item_group!='Raw Material'):
                            create=0
                            delivery_detail[item].delivered_stock_qty+=row.stock_qty
                            delivery_detail[item].delivered_bundle+=row.ts_qty
                            delivery_detail[item].delivered_pieces+=row.pieces
                    raw_material=doc.raw_material
                    for item in range(len(raw_material)):
                        ts_so=(row.against_sales_order if self.doctype=='Delivery Note' else row.sales_order)
                        if(row.item_code==raw_material[item].item and item_group=='Raw Material' and ts_so==raw_material[item].sales_order):
                            raw_material[item].delivered_quantity+=row.qty
                    if(create and item_group!='Raw Material'):
                        delivery_detail.append({
                            'item':row.item_code,
                            'delivered_stock_qty': row.stock_qty,
                            'delivered_bundle':row.ts_qty,
                            'delivered_pieces':row.pieces
                        })
                    doc.update({
                        'raw_material': raw_material,
                        'delivery_detail': delivery_detail
                    })
                    doc.save()
        frappe.db.commit()



def reduce_qty_sitework(self,event):
    if(self.doctype=='Sales Invoice' and self.update_stock==0):
        return
    if(not self.is_return):
        for row in self.items:
            so=(row.against_sales_order if self.doctype=='Delivery Note' else row.sales_order)
            if(so):
                sw=frappe.get_value('Sales Order', so, 'site_work')
                if(sw):
                    item_group=frappe.get_value('Item', row.item_code, 'item_group')
                    doc=frappe.get_doc('Project', sw)
                    delivery_detail=doc.delivery_detail
                    create=1
                    for item in range(len(delivery_detail)):
                        if(row.item_code==delivery_detail[item].item and item_group!='Raw Material'):
                            create=0
                            delivery_detail[item].delivered_stock_qty-=row.stock_qty
                            delivery_detail[item].delivered_bundle-=row.ts_qty
                            delivery_detail[item].delivered_pieces-=row.pieces
                    raw_material=doc.raw_material
                    for item in range(len(raw_material)):
                        ts_so=(row.against_sales_order if self.doctype=='Delivery Note' else row.sales_order)
                        if(row.item_code==raw_material[item].item and item_group=='Raw Material' and ts_so==raw_material[item].sales_order):
                            raw_material[item].delivered_quantity-=row.qty
                    if(create and item_group!='Raw Material'):
                        delivery_detail.append({
                            'item':row.item_code,
                            'delivered_stock_qty': row.stock_qty,
                            'delivered_bundle':row.ts_qty,
                            'delivered_pieces':row.pieces
                        })
                    doc.update({
                        'raw_material': raw_material,
                        'delivery_detail': delivery_detail
                    })
                    doc.save()
        frappe.db.commit()




def update_return_qty_sitework(self,event):
    if(self.doctype=='Sales Invoice' and self.update_stock==0):
        return
    if(self.is_return):
        for row in self.items:
            so=(row.against_sales_order if self.doctype=='Delivery Note' else row.sales_order)
            if(so):
                sw=frappe.get_value('Sales Order', so, 'site_work')
                if(sw):
                    item_group=frappe.get_value('Item', row.item_code, 'item_group')
                    doc=frappe.get_doc('Project', sw)
                    delivery_detail=doc.delivery_detail
                    create=1
                    for item in range(len(delivery_detail)):
                        if(row.item_code==delivery_detail[item].item and item_group!='Raw Material'):
                            create=0
                            delivery_detail[item].returned_stock_qty+=row.stock_qty
                            delivery_detail[item].returned_bundle+=row.ts_qty
                            delivery_detail[item].returned_pieces+=row.pieces
                    raw_material=doc.raw_material
                    for item in range(len(raw_material)):
                        ts_so=(row.against_sales_order if self.doctype=='Delivery Note' else row.sales_order)
                        if(row.item_code==raw_material[item].item and item_group=='Raw Material'  and ts_so==raw_material[item].sales_order):
                            raw_material[item].returned_quantity+=row.qty
                    if(create and item_group!='Raw Material'):
                        delivery_detail.append({
                            'item':row.item_code,
                            'returned_stock_qty':row.stock_qty,
                            'returned_bundle':row.ts_qty,
                            'returned_pieces':row.pieces
                        })
                    doc.update({
                        'raw_material': raw_material,
                        'delivery_detail': delivery_detail
                    })
                    doc.save()
        frappe.db.commit()




def reduce_return_qty_sitework(self,event):
    if(self.doctype=='Sales Invoice' and self.update_stock==0):
        return
    if(self.is_return):
        for row in self.items:
            so=(row.against_sales_order if self.doctype=='Delivery Note' else row.sales_order)
            if(so):
                sw=frappe.get_value('Sales Order', so, 'site_work')
                if(sw):
                    item_group=frappe.get_value('Item', row.item_code, 'item_group')
                    doc=frappe.get_doc('Project', sw)
                    delivery_detail=doc.delivery_detail
                    create=1
                    for item in range(len(delivery_detail)):
                        if(row.item_code==delivery_detail[item].item and item_group!='Raw Material'):
                            create=0
                            delivery_detail[item].returned_stock_qty-=row.stock_qty
                            delivery_detail[item].returned_bundle-=row.ts_qty
                            delivery_detail[item].returned_pieces-=row.pieces
                    raw_material=doc.raw_material
                    for item in range(len(raw_material)):
                        ts_so=(row.against_sales_order if self.doctype=='Delivery Note' else row.sales_order)
                        if(row.item_code==raw_material[item].item and item_group=='Raw Material' and ts_so==raw_material[item].sales_order):
                            raw_material[item].returned_quantity-=row.qty
                    if(create and item_group!='Raw Material'):
                        delivery_detail.append({
                            'item':row.item_code,
                            'returned_stock_qty':row.stock_qty,
                            'returned_bundle':row.ts_qty,
                            'returned_pieces':row.pieces
                        })
                    doc.update({
                        'raw_material': raw_material,
                        'delivery_detail': delivery_detail
                    })
                    doc.save()
        frappe.db.commit()



def update_customer(self,event):
    cus=self.customer
    for row in self.items:
        so=(row.against_sales_order if self.doctype=='Delivery Note' else row.sales_order)
        if(so):
            doc=frappe.get_doc('Sales Order', so)
            if(cus!=doc.customer):
                frappe.db.set(doc, "customer", cus)

def validate(doc,action):
    
    for d in doc.items:
        if d.pieces:
            doc.value_pieces = True
        if d.ts_qty:
            doc.value_bundle = True

        
  
def odometer_validate(doc,action):
    if(doc.return_odometer_value):
        doc.total_distance=doc.return_odometer_value-doc.current_odometer_value
        frappe.db.set_value("Delivery Note" , doc.name, "total_distance",doc.return_odometer_value-doc.current_odometer_value)

@frappe.whitelist()
def make_work_orders(items, delivery_note, company, project=None):
	items = json.loads(items).get("items")
	out = []

	for i in items:
		if not i.get("bom"):
			frappe.throw(("Please select BOM against item {0}").format(i.get("item_code")))
		if not i.get("pending_qty"):
			frappe.throw(("Please select Qty against item {0}").format(i.get("item_code")))

		work_order = frappe.get_doc(
			dict(
				doctype="Work Order",
				production_item=i["item_code"],
				bom_no=i.get("bom"),
				qty=i["pending_qty"],
				company=company,
				delivery_note=delivery_note,
				delivery_note_item=i["delivery_note_item"],
				project=project,
				fg_warehouse=i["warehouse"],
				description=i["description"],
                priority = "Low Priority"
			)
		).insert()
		work_order.set_work_order_operations()
		work_order.flags.ignore_mandatory = True
		work_order.save()
		out.append(work_order)

	return [p.name for p in out]
@frappe.whitelist()

def get_work_order_items(self, for_raw_material_request=0):
    self = json.loads(self)
    items = []
    item_codes = [i['item_code'] for i in self['items']]
    for table in [self['items'], self['packed_items']]:
        for i in table:
            bom = get_default_bom(i['item_code'])
            stock_qty = i['qty'] if i['doctype'] == "Packed Item" else i['stock_qty']
            pending_qty = stock_qty
            if pending_qty and i['item_code']:
                items.append(
                    dict(
                        name=i['name'],
                        item_code=i['item_code'],
                        description=i['description'],
                        bom=bom or "",
                        warehouse=i['warehouse'],
                        pending_qty=pending_qty,
                        required_qty=pending_qty if for_raw_material_request else 0,
                        delivery_note_item=i['name'],
                    )
                )

    return items

@frappe.whitelist()
def get_item_loading_cost(items, len, work=None):
    items=json.loads(items)
    multiply=1
    if(work == "Both Loading and Unloading"):
        multiply=2
    loading_cost=0
    for i in items:
        if(i.get('dont_include_in_loadman_cost') == 1):continue
        loading_cost += (frappe.get_value('Item', i.get('item_code'), 'loading_cost') or 0)*i.get('qty')
    return (loading_cost*multiply)/flt(len)