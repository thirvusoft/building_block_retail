# Copyright (c) 2022, Thirvusoft and contributors
# For license information, please see license.txt

import frappe


def execute(filters={}):
	columns, data = get_columns() or [], get_data(filters) or []
	chart = get_chart_data(data)
	return columns, data , 'Here all Quantities are mentioned in <b>Nos</b>', chart


def get_columns():
	columns = [
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
			'fieldname':'total_planned_qty',
			'label':'Total Planned Qty',
			'fieldtype':'Float',
			'width':150,
		},
		{
			'fieldname':'total_prod_qty',
			'label':'Total Production Qty',
			'fieldtype':'Float',
			'width':150,
		},
		{
			'fieldname':'today_planned_qty',
			'label':'Today Planned Qty',
			'fieldtype':'Float',
			'width':150,
		},
		{
			'fieldname':'today_prod_qty',
			'label':'Today Produced Qty',
			'fieldtype':'Float',
			'width':150,
		},
		{
			'fieldname':'stock_not_added',
			'label':'Stock Not Added',
			'fieldtype':'Float',
			'width':150,
		},
	]
	return columns

def get_chart_data(data):
	if(len(data)):
		label = [i['item'] for i in data]
		today_prod_qty = [i['today_prod_qty'] for i in data]
		planned_qty = [i['today_planned_qty'] for i in data]
		chart_data = {
			"data": {
				"labels": label,
				"datasets": [{"name": "Planned Qty", "values": planned_qty},{"name": "Qty Produced", "values": today_prod_qty}],
			},
			"type": "line",
			'colors':['green','blue'],
			'lineOptions':{'hideDots':0, 'dotSize':6, 'regionFill':1}
		}

		return chart_data

def get_data(filters):
	final_data = []
	so_filt = {'docstatus':1, 'per_delivered':['<', 99]}
	if(so:=filters.get('sales_order')):
		so_filt['name'] = so
	sales_order = frappe.db.get_all('Sales Order', filters=so_filt, pluck='name')
	wo_filt = {'docstatus':1, 'sales_order':['in', sales_order]}
	if(filters.get('item_code')):
		wo_filt['production_item'] = filters.get('item_code')
	work_order = frappe.db.get_all('Work Order', filters=wo_filt, pluck='name')
	for wo in work_order:
		job_card = frappe.db.get_all('Job Card', filters={'docstatus':['!=', 2], 'work_order':wo}, pluck='name')
		jc_filter = {'docstatus':['!=', 2], 'parent':['in', job_card], 'parentfield':'time_logs'}
		if(filters.get('from_date')):
			jc_filter['from_time'] = ['>=', filters.get('from_date')]
		if(filters.get('to_date')):
			jc_filter['to_time'] = ['<=', filters.get('to_date')]
		if(filters.get('from_date') and filters.get('to_date')):
			jc_filter['from_time'] = ['between', (filters.get('from_date'), filters.get('to_date'))]
			jc_filter['to_time'] = ['between', (filters.get('from_date'), filters.get('to_date'))]
		
		jc_time_logs = frappe.db.get_all('Job Card Time Log', filters=jc_filter, fields=['sum(final_qty) as today_prod_qty', 'parent', 'cast(from_time as date) as date'], )
		for jc in jc_time_logs:
			data = frappe.db.get_all('Work Order', filters={'name':wo}, fields=['name', 'sales_order', 'qty as total_planned_qty', 'produced_qty as total_prod_qty', 'production_item as item'])
			for i in data:
				jc_filt = {'docstatus':['!=', 2],'work_order':i['name']}
				if(filters.get('from_date')):
					jc_filt['posting_date'] = ['>=', filters.get('from_date')]
				if(filters.get('to_date')):
					jc_filt['posting_date'] = ['<=', filters.get('to_date')]
				if(filters.get('from_date') and filters.get('to_date')):
					jc_filt['posting_date'] = ['between', (filters.get('from_date'), filters.get('to_date'))]
		
				i['today_planned_qty'] = sum(frappe.db.get_all('Job Card', filters=jc_filt, pluck='for_quantity'))
				i['stock_not_added'] = sum(frappe.db.get_all('Job Card', filters={'docstatus':['!=', 2], 'work_order':i['name']}, pluck='total_completed_qty')) - sum(frappe.db.get_all('Stock Entry', filters={'work_order':i['name'], 'docstatus':1}, pluck='fg_completed_qty'))
			if(len(data)):
				jc.update(data[0])
		final_data += jc_time_logs
	return final_data