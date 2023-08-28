
__version__ = '0.0.1'

import frappe
from frappe.utils.data import flt


def get_reserved_qty(item_code, warehouse, posting_date=None, posting_time=None, ignored_sales_order=None):
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