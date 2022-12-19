// Copyright (c) 2022, Thirvusoft and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Get Possible Delivery Date of Item"] = {
	"filters": [
		{
			'fieldname':'item_code',
			'label':'Item',
			'reqd':1,
			'filters':{'disabled':0, 'has_variants':0, 'parent_item_group':'Products'},
			'fieldtype':'Link',
			'options':'Item'
		},
		{
			'fieldname':'order_qty',
			'label':'Order Qty(In Stock UOM)',
			'fieldtype':'Float',
		},
	]
};
