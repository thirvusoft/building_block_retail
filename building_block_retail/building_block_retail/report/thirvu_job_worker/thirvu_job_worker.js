// Copyright (c) 2022, Thirvusoft and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Thirvu Job Worker"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_days(frappe.datetime.get_today(), -30),
			"width": "80",
			"reqd":1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"width": "80",
			"reqd":1

		},
		{
			"fieldname":"site_name",
			"label": __("Site Name"),
			"fieldtype": "Link",
			"options": "Project",
			"width": "100"
		},
		{
			"fieldname":"employee",
			"label": __("Job Worker"),
			"fieldtype": "Link",
			"options": "Employee",
			"width": "100"
		}


	],
	"formatter": function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if(column.fieldname == 'status'){
			if(value == 'Total'){
				value = "<b style=color:orange;>Total</b>"
			}
			else{
				value = "<span style=colour:"+frappe.utils.guess_colour(data['status'])+";>"+value+" </span>"
			}
			
			return value;
		}
		if(data['status'] == "Total"){
			value = "<b style=color:#1d4157>"+value+"</b>"
			return value;
		}
		
		return value;
	},
};
