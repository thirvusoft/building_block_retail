// Copyright (c) 2022, Thirvusoft and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["TS Sales Partner Payable Summary"] = {
	"filters": [
		{
			'fieldname':'sales_partner',
			'label':'Sales Partner',
			'fieldtype':'Link',
			'options':'Sales Partner'
		},
		{
			'fieldname':'partner_type',
			'label':'Partner Type',
			'fieldtype':'Link',
			'options':'Sales Partner Type'
		},
		{
			'fieldname':'territory',
			'label':'Territory',
			'fieldtype':'Link',
			'options':'Territory'
		}
	]
};
