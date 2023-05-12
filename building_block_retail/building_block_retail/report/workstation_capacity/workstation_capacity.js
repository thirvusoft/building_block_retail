// Copyright (c) 2023, Thirvusoft and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Workstation Capacity"] = {
	"filters": [
		{
			fieldname:'from_date',
			label:'From Date',
			fieldtype:'Date',
		},
		{
			fieldname:'to_date',
			label:'To Date',
			fieldtype:'Date',
		},
		{
			fieldname:'workstation',
			label:'Workstation',
			fieldtype:'Link',
			options:'Workstation'
		},
		{
			fieldname:'item',
			label:'Item',
			fieldtype:'Link',
			options:'Item'
		},
		{
			fieldname:'employee',
			label:'Employee',
			fieldtype:'Link',
			options:'Employee'
		},
	],
	"formatter": function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if(data && data.effective_percent < 100 && column.fieldname == "effective_percent"){
			value = "<p style='color:red;font-weight:bold'>" + value + "</p>";
		}
		if(data && data.effective_percent == 100 && column.fieldname == "effective_percent"){
			value = "<p style='color:blue;font-weight:bold'>" + value + "</p>";
		}
		if(data && data.effective_percent > 100 && column.fieldname == "effective_percent"){
			value = "<p style='color:green;font-weight:bold'>" + value + "</p>";
		}
		
		return value;
	},
};
