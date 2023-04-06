from copy import copy
from dataclasses import field
import frappe
import json
from frappe.model.mapper import get_mapped_doc
from frappe.utils.csvutils import getlink
from erpnext.stock.get_item_details import get_default_bom
from frappe.utils.data import flt


@frappe.whitelist()
def get_item_value(doctype):
    uom=frappe.get_doc('Item',doctype)
    conv=0
    if(uom.item_group=='Raw Material'):
        conv=1
    else:
        if(not uom.sales_uom):
                frappe.throw("Please Enter Sales Uom for an item:"+getlink('Item', doctype))
        for row in uom.uoms:
            if(row.uom==uom.sales_uom):
                conv=row.conversion_factor
        if(not conv):
            frappe.throw('Please enter UOM conversion for Square foot in item: '+getlink('Item', doctype))
    res={
        'item_name':frappe.get_value('Item',doctype,'item_name'),
        'description':frappe.get_value('Item',doctype,'description'),
        'uom':frappe.get_value('Item',doctype,'sales_uom'),
        'uom_conversion':conv
    }
    return res
    
@frappe.whitelist()
def create_site(doc):
    doc=json.loads(doc)
    create=False
    if(doc['type']=='Pavers'):
        for row in (doc['pavers'] or []):
            if(row["work"]!="Supply Only"):
                create=True
    if(doc['type']=='Compound Wall'):
        for row in (doc['compoun_walls'] or []):
            if(row["work"]!="Supply Only"):
                create=True
    if(doc['work']!="Supply Only" and create):
        supervisor=doc.get('supervisor_name') if('supervisor_name' in doc) else ''
        pavers=[]
        compoun_walls=[]
        if(doc['type']=='Pavers'):
            pavers=[{
                    'item':row['item'],
                    'required_area':row['required_area'],
                    'area_per_bundle':row['area_per_bundle'],
                    'number_of_bundle':row['number_of_bundle'],
                    'allocated_paver_area':row['allocated_paver_area'],
                    'rate':row['rate'],
                    'amount':row['amount'],
                    'work': row['work'],
                    'sales_order':doc['name'],
                    'warehouse':row['warehouse'] if(row.get('warehouse')) else doc.get('set_warehouse')
                    } for row in doc['pavers']]
        if(doc['type']=='Compound Wall'):
            compoun_walls=[{
                    'item':row['item'],
                    'compound_wall_type':row['compound_wall_type'],
                    'allocated_ft':row['allocated_ft'],
                    'rate':row['rate'],
                    'amount':row['amount'],
                    'work': row['work'],
                    'sales_order':doc['name'],
                    'warehouse':row['warehouse'] if(row.get('warehouse')) else doc.get('set_warehouse')
                    } for row in doc['compoun_walls']]
        raw_material=[{
                'item':row['item'],
                'qty':row['qty'],
                'uom':row['uom'],
                'rate':row['rate'],
                'amount':row['amount'],
                'sales_order':doc['name']
                } for row in doc['raw_materials']]
        site_work=frappe.get_doc('Project',doc['site_work'])
        total_area=0
        completed_area=0
        
        for item in (site_work.get('item_details') or []):
            total_area+=item.required_area
        for item in pavers:
            total_area+=item['required_area']
        for item in (site_work.get('item_details_compound_wall') or []):
            total_area+=item.allocated_ft
        for item in compoun_walls:
            total_area+=item['allocated_ft']
        for item in (site_work.get('job_worker') or []):
            completed_area+=item.sqft_allocated
        
        site_work.update({
            'customer': doc['customer'] or '',
            'supervisor': doc.get('supervisor') if('supervisor' in doc) else '',
            'supervisor_name': supervisor,
            'item_details': (site_work.get('item_details') or []) +pavers,
            'item_details_compound_wall': (site_work.get('item_details_compound_wall') or []) +compoun_walls,
            'raw_material': (site_work.get('raw_material') or []) + raw_material,
            'total_required_area': total_area,
            'total_completed_area': completed_area,
            'completed': (completed_area/total_area)*100,
            'distance':(site_work.get('distance') or 0)+(doc.get('distance') or 0)
        })
        if(doc['is_multi_customer']):
            sw_cust=[cus.customer for cus in (site_work.get('customer_name') or [] )]
            customer=[]
            for cust in doc['customers_name']:
                if(cust['customer'] not in sw_cust):
                    customer.append({'customer':cust['customer']})
            site_work.update({
                'customer_name': (site_work.get('customer_name') or [] ) + customer
            })
        site_work.update({
            'per_delivered':doc.get('per_delivered') or 0
        })
        site_work.save()
        frappe.db.commit()
        return 1


@frappe.whitelist()
def create_property():
    doc=frappe.new_doc('Property Setter')
    doc.update({
        "doctype_or_field": "DocField",
        "doc_type":"Sales Order",
        "field_name":"customer",
        "property":"reqd",
        "value":0
    })
    doc.save()
    frappe.db.commit()
    return doc.name
   
   
@frappe.whitelist()
def remove_property(prop_name):
    frappe.delete_doc('Property Setter',prop_name)
    frappe.db.commit()


@frappe.whitelist()
def update_temporary_customer(customer, sales_order):
    doc=frappe.get_doc('Sales Order',sales_order)
    frappe.db.set(doc, "customer", customer)

@frappe.whitelist()
def get_customer_list(sales_order):
    doc=frappe.get_doc('Sales Order', sales_order)
    customer=[cust.customer for cust in doc.customers_name]
    return '\n'.join(customer)
    
def remove_project_fields(self,event):
    project=self.site_work
    if(project):
        doc=frappe.get_doc('Project',project)
        paver=doc.get('item_details') or []
        raw_material=doc.get('raw_material')
        new_paver=[]
        new_rm=[]
        for item in paver:
            if(item.sales_order!=self.name):
                new_paver.append(item)
        for item in raw_material:
            if(item.sales_order!=self.name):
                new_rm.append(item)
                
                
        total_area=0
        completed_area=0
        for item in (new_paver or []):
            total_area+=(item.get('required_area') or 0)
        for item in (doc.get('job_worker') or []):
            completed_area+=(item.get('sqft_allocated') or 0)
        
        if(total_area):
            percent=(completed_area/total_area)*100
        else:
            percent=0
        doc.update({
            'item_details':new_paver,
            'raw_material':new_rm,
            'total_required_area': total_area,
            'total_completed_area': completed_area,
            'completed': percent
        })
        doc.save()
        frappe.db.commit()



@frappe.whitelist()
def get_item_rate(item='', uom=None, selling=1, check_for_uom=None):
    filter1={'selling': selling}
    if(uom):
        filter1['uom']=uom
    
    if(not item or item not in frappe.get_all('Item Price', filter1, pluck='item_code')):
        return 0
    filter1['uom'] = check_for_uom
    filter1['item_code']=item
    if(frappe.db.exists('Item Price', filter1) and check_for_uom):
        return frappe.db.get_value('Item Price', filter1, 'price_list_rate')
    elif(check_for_uom):
        del filter1['uom']
        uom, rate = frappe.db.get_value('Item Price', filter1, ['uom', 'price_list_rate'])
        stock_uom = frappe.db.get_value('Item', item, 'stock_uom')
        final_conv = 1
        if(uom != stock_uom):
            conv1= frappe.db.get_value('UOM Conversion Detail', {'parent':item, 'uom':stock_uom}, 'conversion_factor')
            conv2= frappe.db.get_value('UOM Conversion Detail', {'parent':item, 'uom':uom}, 'conversion_factor')
            final_conv = conv1/conv2
        conv = frappe.db.get_value('UOM Conversion Detail', {'parent':item, 'uom':check_for_uom}, 'conversion_factor') or 0
        return rate * conv * final_conv

    
    doc=frappe.get_last_doc('Item Price', filter1)
    return doc.price_list_rate or 0
    
        
@frappe.whitelist()
def get_stock_availability(items):
    items = json.loads(items)
    stock_availability = []
    for i in items:
        if(frappe.get_value('Item', i.get('item_code'),'item_group') != "Raw Material"):
            conv=1
            
            res_qty, act_qty = frappe.db.get_value("Bin",{'warehouse':i.get('warehouse'), 'item_code':i.get('item_code'), 'stock_uom':i.get('stock_uom')},['reserved_qty','actual_qty'])
            qty, planned_production_qty = 0, 0
            planned_production_qty = sum(frappe.get_all("Work Order", filters={'docstatus':1, 'production_item':i.get('item_code'),'sales_order':i.get("parent")},pluck='qty'))
            currently_produced_qty = sum(frappe.get_all("Work Order", filters={'docstatus':1, 'production_item':i.get('item_code'),'sales_order':i.get("parent")},pluck='produced_qty'))
            if(res_qty<act_qty):qty = qty = act_qty-res_qty
            stock_availability.append({'item':i.get('item_code'),'warehouse':i.get('warehouse'),'qty':float(qty or 0)*conv,'ordered_qty':round(float(i.get('stock_qty') or 0))*conv,'stock_uom':i.get('stock_uom'),'planned_production_qty':float(planned_production_qty or 0)*conv, 'currently_produced_qty':float(currently_produced_qty or 0)*conv})
    return stock_availability

@frappe.whitelist()
def remove_raw_materials_from_items(doc):
    doc = json.loads(doc)
    items = []
    raw = [i['item'] for i in doc['raw_materials']]
    for i in doc['items']:
        if(i['item_code'] not in raw):items.append(i)
    doc.update({
        'items':items
    })
    return doc

@frappe.whitelist()
def get_work_order_items(self, for_raw_material_request=0):
    self = json.loads(self)
    """Returns items with BOM that already do not have a linked work order"""
    items = []
    item_codes = [i['item_code'] for i in self['items']]
    product_bundle_parents = [
        pb.new_item_code
        for pb in frappe.get_all(
            "Product Bundle", {"new_item_code": ["in", item_codes]}, ["new_item_code"]
        )
    ]

    for table in [self['items'], self['packed_items']]:
        for i in table:
            bom = get_default_bom(i['item_code'])
            stock_qty = i['qty'] if i['doctype'] == "Packed Item" else i['stock_qty']

            if not for_raw_material_request:
                total_work_order_qty = flt(
                    frappe.db.sql(
                        """select sum(qty) from `tabWork Order`
                    where production_item=%s and sales_order=%s and sales_order_item = %s and docstatus<2""",
                        (i['item_code'], self['name'], i['name']),
                    )[0][0]
                )
                pending_qty = stock_qty - total_work_order_qty
            else:
                pending_qty = stock_qty

            if pending_qty > 0 and i['item_code'] not in product_bundle_parents:
                items.append(
                    dict(
                        name=i['name'],
                        item_code=i['item_code'],
                        description=i['description'],
                        bom=bom or "",
                        warehouse=i['warehouse'],
                        req_qty=pending_qty,
                        required_qty=pending_qty if for_raw_material_request else 0,
                        sales_order_item=i['name'],
                    )
                )
    item = get_stock_and_priority(items)
    return item

def get_stock_and_priority(items):
    item = []
    idx=0
    for row in items:
        conv=1
        if(frappe.get_value('Item', row.get('item_code'),'item_group') != "Raw Material"):
            buffer = frappe.get_value("Item",row['item_code'], 'over_production_allowance')
            order_qty = frappe.get_value("Sales Order Item",row['name'], 'stock_qty')
            stock = frappe.get_all("Bin", filters={'item_code': row['item_code'], 'warehouse':row.get('warehouse')},fields=['reserved_qty', 'actual_qty'])
            res, avail_qty, stock_taken, req_qty= -order_qty,0,0,0
            se_completed_qty=get_pre_work_order_completed_qty(row['name'])
            priority = ''
            for i in stock:
                res+=i['reserved_qty']
                avail_qty+=i['actual_qty']
            act_qty = avail_qty - res - se_completed_qty
            if(act_qty<=0):
                act_qty=0
                stock_taken=0
                req_qty=row['req_qty']
                priority = 'Urgent Priority'
            if(act_qty>row['req_qty']):
                stock_taken = row['req_qty']
                req_qty = row['req_qty']
                priority = 'Low Priority'
            if(act_qty>0 and act_qty<row['req_qty']):
                priority = 'Low Priority'
                req_qty = act_qty
                stock_taken = act_qty
                copy_req_qty = row['req_qty']
                row['req_qty'] *= conv
                row['req_qty'] = round(row['req_qty'])
                new_row=copy(row)
                new_row['stock_availability'] = 0
                new_row['stock_taken'] = 0
                new_row['pending_qty'] = round((copy_req_qty - act_qty)*conv)
                new_row['buffer_qty'] = round(round((copy_req_qty - act_qty)*conv)*buffer/100)
                new_row['priority'] = 'Urgent Priority'
                item.append(new_row)
                row['req_qty'] = copy_req_qty
                
            items[idx]['stock_availability'] = round(act_qty*conv)
            items[idx]['stock_taken'] = round(stock_taken*conv)
            items[idx]['pending_qty'] = round(req_qty*conv) 
            items[idx]['buffer_qty'] = round(round(req_qty*conv) * buffer/100)
            items[idx]['priority'] = priority
            items[idx]['req_qty'] *= conv
            items[idx]['req_qty'] = round(items[idx]['req_qty'])
            item.append(items[idx])
            idx+=1
    return item

def get_pre_work_order_completed_qty(so_child):
    so = frappe.get_value('Sales Order Item', so_child, 'parent')
    wo = frappe.get_all("Work Order",filters={'sales_order':so}, pluck='name')
    qty=0
    for i in wo:
        qty += (sum(frappe.get_all("Stock Entry", filters={'work_order':i}, pluck='fg_completed_qty')) or 0)
    return qty

@frappe.whitelist()
def make_work_orders(items, sales_order, company, project=None):
    """Make Work Orders against the given Sales Order for the given `items`"""
    items = json.loads(items).get("items")
    out = []

    for i in items:
        if not i.get("bom"):
            frappe.throw(("Please select BOM against item {0}").format(i.get("item_code")))
        if not i.get("pending_qty"):
            frappe.throw(("Please select Qty against item {0}").format(i.get("item_code")))
        conv=1
        work_order = frappe.get_doc(
            dict(
                doctype="Work Order",
                production_item=i["item_code"],
                bom_no=i.get("bom"),
                qty=(i["pending_qty"]+ (i["buffer_qty"] or 0) / conv),
                ts_qty_to_manufacture = i["pending_qty"]+(i["buffer_qty"] or 0),
                company=company,
                use_multi_level_bom = 0,
                sales_order=sales_order,
                sales_order_item=i["sales_order_item"],
                project=project,
                fg_warehouse=i["warehouse"],
                description=i["description"],
                priority=i['priority']
            )
        ).insert()
        work_order.set_work_order_operations()
        work_order.flags.ignore_mandatory = True
        work_order.save()
        out.append(work_order)

    return [p.name for p in out]


#on submit
def check_opportunity(doc,event):
    opportunity=frappe.get_all("Opportunity",filters={"party_name":doc.customer},pluck="name",order_by="`creation` DESC",limit=1)
    if opportunity:
        opp_doc=frappe.get_doc("Opportunity",opportunity[0])
        if opp_doc.status != "Ordered":
            opp_doc.status="Ordered"
            opp_doc.save()

#Validate
def add_price_list(doc, event):
    for i in doc.items:
        if(i.item_group == 'Raw Material' and not frappe.db.exists('Item Price', {'selling':1, 'price_list':doc.selling_price_list, 'item_code':i.item_code, 'uom':i.uom})):
            pl = frappe.new_doc("Item Price")
            pl.update({
                'item_code': i.item_code,
                'uom': i.uom,
                'price_list':doc.selling_price_list,
                'selling':1,
                'price_list_rate': i.rate
            })
            pl.save(ignore_permissions=True)


@frappe.whitelist()
def branch_list(company):
    branch_filter=[]
    branch_list=frappe.get_list(
		"Accounting Dimension Detail",
		filters={"parent":"Branch","company":company},
        fields=["default_dimension"]
    )
    for rows in branch_list:
        branch_filter.append(rows.default_dimension)
   
    return branch_filter