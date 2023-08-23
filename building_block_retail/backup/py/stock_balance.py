# apps/erpnext/erpnext/stock/report/stock_balance/stock_balance.py

def get_columns(filters):
	"""return columns"""

	svpb_admin = 'SVPB Admin' in frappe.get_roles()
	extra_width = 50 if not svpb_admin else 0

	columns = [
		{
			"label": _("Item"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": extra_width + 100,
		},
		{"label": _("Item Name"), "fieldname": "item_name", "width": extra_width + 150},
		{
			"label": _("Item Group"),
			"fieldname": "item_group",
			"fieldtype": "Link",
			"options": "Item Group",
			"width": extra_width + 100,
		},
		{
			"label": _("Warehouse"),
			"fieldname": "warehouse",
			"fieldtype": "Link",
			"options": "Warehouse",
			"width": extra_width + 100,
		},
		{
			"label": _("Stock UOM"),
			"fieldname": "stock_uom",
			"fieldtype": "Link",
			"options": "UOM",
			"width": extra_width + 90,
		},
		{
			"label": _("Balance Qty"),
			"fieldname": "bal_qty",
			"fieldtype": "Float",
			"width": extra_width + 100,
			"convertible": "qty",
		},
		{
			"label": _("Balance Value"),
			"fieldname": "bal_val",
			"fieldtype": "Currency",
			"width": 100,
			"options": "currency",
		 	"hidden": not svpb_admin
		},
		{
			"label": _("Opening Qty"),
			"fieldname": "opening_qty",
			"fieldtype": "Float",
			"width": 100,
			"convertible": "qty",
		 	"hidden": not svpb_admin
		},
		{
			"label": _("Opening Value"),
			"fieldname": "opening_val",
			"fieldtype": "Currency",
			"width": 110,
			"options": "currency",
		 	"hidden": not svpb_admin
		},
		{
			"label": _("In Qty"),
			"fieldname": "in_qty",
			"fieldtype": "Float",
			"width": 80,
			"convertible": "qty",
		 	"hidden": not svpb_admin
		},
		{"label": _("In Value"), "fieldname": "in_val", "fieldtype": "Float", "width": 80, "hidden": not svpb_admin},
		{
			"label": _("Out Qty"),
			"fieldname": "out_qty",
			"fieldtype": "Float",
			"width": 80,
			"convertible": "qty",
		 	"hidden": not svpb_admin
		},
		{"label": _("Out Value"), "fieldname": "out_val", "fieldtype": "Float", "width": 80, "hidden": not svpb_admin},
		{
			"label": _("Valuation Rate"),
			"fieldname": "val_rate",
			"fieldtype": "Currency",
			"width": 90,
			"convertible": "rate",
			"options": "currency",
		 	"hidden": not svpb_admin
		},
		{
			"label": _("Reorder Level"),
			"fieldname": "reorder_level",
			"fieldtype": "Float",
			"width": 80,
			"convertible": "qty",
			"hidden": not svpb_admin
		},
		{
			"label": _("Reorder Qty"),
			"fieldname": "reorder_qty",
			"fieldtype": "Float",
			"width": 80,
			"convertible": "qty",
		 	"hidden": not svpb_admin
		},
		{
			"label": _("Company"),
			"fieldname": "company",
			"fieldtype": "Link",
			"options": "Company",
			"width": 100,
		 	"hidden": not svpb_admin
		},
	]

	if filters.get("show_stock_ageing_data"):
		columns += [
			{"label": _("Average Age"), "fieldname": "average_age", "width": 100},
			{"label": _("Earliest Age"), "fieldname": "earliest_age", "width": 100},
			{"label": _("Latest Age"), "fieldname": "latest_age", "width": 100},
		]

	if filters.get("show_variant_attributes"):
		columns += [
			{"label": att_name, "fieldname": att_name, "width": 100}
			for att_name in get_variants_attributes()
		]

	return columns