# Copyright (c) 2022, Thirvusoft and contributors
# For license information, please see license.txt

import frappe


def execute(filters={}):
	columns, data = get_columns() or [], get_data(filters) or []
	return columns, data , 'Here all Quantities are mentioned in <b>Nos</b>'


def get_columns():
	columns = [
		{
			'fieldname':'date',
			'label':'Date',
			'fieldtype':'Date',
			'width':200,
		},
		{
			'fieldname':'sales_order',
			'fieldtype':'Link',
			'label':'Sales Order',
			'options':'Sales Order',
			'width':200,
		},
		{
			'fieldname':'item',
			'label':'Item',
			'options':'Item',
			'fieldtype':'Link',
			'width':200,
		},
		{
			'fieldname':'today_prod_qty',
			'label':'Today Produced Qty',
			'fieldtype':'Float',
			'width':200,
		},
		{
			'fieldname':'total_prod_qty',
			'label':'Total Production Qty',
			'fieldtype':'Float',
			'width':200,
		},
		{
			'fieldname':'total_planned_qty',
			'label':'Total Planned Qty',
			'fieldtype':'Float',
			'width':200,
		},
	]
	return columns

def get_data(filters):
	final_data = []
	so_filt = {'docstatus':1, 'per_delivered':['<', 99]}
	if(so:=filters.get('sales_order')):
		so_filt['name'] = so
	sales_order = frappe.db.get_all('Sales Order', filters=so_filt, pluck='name')
	work_order = frappe.db.get_all('Work Order', filters={'docstatus':1, 'sales_order':['in', sales_order]}, pluck='name')
	for wo in work_order:
		job_card = frappe.db.get_all('Job Card', filters={'docstatus':1, 'work_order':wo}, pluck='name')
		jc_filter = {'docstatus':1, 'parent':['in', job_card]}
		if(filters.get('from_date')):
			jc_filter['from_time'] = ['>=', filters.get('from_date')]
		if(filters.get('to_date')):
			jc_filter['to_time'] = ['<=', filters.get('to_date')]
		if(filters.get('from_date') and filters.get('to_date')):
			jc_filter['from_time'] = ['between', (filters.get('from_date'), filters.get('to_date'))]
			jc_filter['to_time'] = ['between', (filters.get('from_date'), filters.get('to_date'))]
		
		jc_time_logs = frappe.db.get_all('Job Card Time Log', filters=jc_filter, fields=['completed_qty as today_prod_qty', 'parent', 'from_time as date'])
		for jc in jc_time_logs:
			# wo = frappe.db.get_value('Job Card', jc['parent'], 'work_order')
			data = frappe.db.get_all('Work Order', filters={'name':wo}, fields=['sales_order', 'qty as total_planned_qty', 'produced_qty as total_prod_qty', 'production_item as item'])
			if(len(data)):
				jc.update(data[0])
		final_data += jc_time_logs
		frappe.errprint(jc_time_logs)
	return final_data