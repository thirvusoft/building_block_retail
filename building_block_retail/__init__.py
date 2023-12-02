
__version__ = '0.0.1'

def get_reserved_qty(item_code, warehouse, posting_date=None, posting_time=None, ignored_sales_order=None):
	import frappe
	from frappe.utils.data import flt
	if not posting_date:
		posting_date = frappe.utils.nowdate()
	if not posting_time:
		posting_time = "23:59:59"

	posting_time = (posting_time or '').split('.')[0]

	reserved_qty = frappe.db.sql("""
		select
			sum(dnpi_qty * ((so_item_qty - so_item_delivered_qty) / so_item_qty))
		from
			(
				(select
					qty as dnpi_qty,
					(
						select qty from `tabSales Order Item`
						where name = dnpi.parent_detail_docname
						and (delivered_by_supplier is null or delivered_by_supplier = 0)
					) as so_item_qty,
					(
						select delivered_qty from `tabSales Order Item`
						where name = dnpi.parent_detail_docname
						and delivered_by_supplier = 0
					) as so_item_delivered_qty,
					parent, name
				from
				(
					select qty, parent_detail_docname, parent, name
					from `tabPacked Item` dnpi_in
					where item_code = %(item_code)s and warehouse = %(warehouse)s
					and parenttype="Sales Order"
					and item_code != parent_item
					and exists (select * from `tabSales Order` so
					where name = dnpi_in.parent and docstatus = 1 and status != 'Closed'
			       	and TIMESTAMP(so.transaction_date, TIME(so.creation)) < TIMESTAMP(DATE(%(posting_date)s), TIME(%(posting_time)s)) AND so.name != %(ignored_sales_order)s )
				) dnpi)
			union
				(select stock_qty as dnpi_qty, qty as so_item_qty,
					delivered_qty as so_item_delivered_qty, parent, name
				from `tabSales Order Item` so_item
				where item_code = %(item_code)s and warehouse = %(warehouse)s
				and (so_item.delivered_by_supplier is null or so_item.delivered_by_supplier = 0)
				and exists(select * from `tabSales Order` so
					where so.name = so_item.parent and so.docstatus = 1
					and so.status != 'Closed'
                   	and TIMESTAMP(so.transaction_date, TIME(so.creation)) < TIMESTAMP(DATE(%(posting_date)s), TIME(%(posting_time)s)) AND so.name != %(ignored_sales_order)s ))
			) tab
		where
			so_item_qty >= so_item_delivered_qty
	""", {
		'item_code': item_code,
		'warehouse': warehouse,
		'posting_date': posting_date,
		'posting_time': posting_time,
		'ignored_sales_order': ignored_sales_order
    })

	return flt(reserved_qty[0][0]) if reserved_qty else 0

def uom_conversion(item : str, from_uom='', from_qty=0.0, to_uom='', throw_err=True) -> float:
	''' 
		For converting rate, pass from as to and to as from uoms
	'''
	import frappe
	from frappe.utils.data import flt
	if (not to_uom):
		return from_qty
	if(not from_uom):
		from_uom = frappe.get_value('Item', item, 'stock_uom')

	from_conv = frappe.db.get_value("UOM Conversion Detail", {'parent': item, 'parenttype': 'Item', 'uom': from_uom}, 'conversion_factor') or 0
	to_conv = frappe.db.get_value("UOM Conversion Detail", {'parent': item, 'parenttype': 'Item', 'uom': to_uom}, 'conversion_factor') or 0

	if(not from_conv):
		if throw_err:
			frappe.throw(f"Please enter value for {frappe.bold(from_uom)} conversion in {frappe.bold(item)}")
		else:
			return 0.0
	
	if(not to_conv):
		if throw_err:
			frappe.throw(f"Please enter value for {frappe.bold(to_uom)} conversion in {frappe.bold(item)}")
		else:
			return 0.0
		
	res = (float(from_qty) * from_conv) / to_conv
	return res
