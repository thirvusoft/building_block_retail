// Copyright (c) 2022, Thirvusoft and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Daily Production summary"] = {
	"filters": [
		{
			fieldname:'sales_order',
			label:'Sales Order',
			fieldtype:'Link',
			options:'Sales Order',
			filters:{'docstatus':1},
		},
		{
			fieldname:'item_code',
			label:'Item',
			fieldtype:'Link',
			options:'Item',
			filters:{'disabled':0, 'parent_item_group':'Products'},
		},
		{
			fieldname:'from_date',
			label:'From Date',
			fieldtype:'Date',
			default:frappe.datetime.get_today(),
		},
		{
			fieldname:'to_date',
			label:'To Date',
			fieldtype:'Date',
			default:frappe.datetime.get_today(),
		}
	]
};
