# Copyright (c) 2023, Thirvusoft and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data

def get_columns():
	columns = [
		{
			'fieldname':'date',
			'label':'Date',
			'fieldtype':'Date',
			'width':150
		},
		{
			'fieldname':'job_card',
			'label':'Job Card',
			'fieldtype':'Link',
			'options':'Job Card',
			'width':150
		},
		{
			'fieldname':'employee',
			'label':'Employee',
			'fieldtype':'Link',
			'options':'Employee',
			'width':200
		},
		{
			'fieldname':'item_code',
			'label':'Item',
			'fieldtype':'Link',
			'options':'Item',
			'width':250
		},
		{
			'fieldname':'workstation',
			'label':'Workstation',
			'fieldtype':'Link',
			'options':'Workstation',
			'width':100
		},
		{
			'fieldname':'total_hrs',
			'label':'Hrs Worked',
			'fieldtype':'Float',
			'width':100
		},
		{
			'fieldname':'expected_qty',
			'label':'Expected Qty',
			'fieldtype':'Float',
			'width':100
		},
		{
			'fieldname':'actual_qty',
			'label':'Actual Qty',
			'fieldtype':'Float',
			'width':100
		},
		{
			'fieldname':'effective_percent',
			'label':'Efficient',
			'fieldtype':'Data',
			'width':100
		},
	]
	return columns

def get_data(filters={}):
	data = [{}]
	condition = " jct.parentfield = 'time_logs'"
	if(filters.get('from_date') and filters.get('to_date')):
		condition += f""" AND jc.posting_date >= "{filters['from_date']}" and jc.posting_date <= "{filters['to_date']}" """
	elif(filters.get('from_date')):
		condition += f""" AND jc.posting_date >= "{filters['from_date']}" """
	elif(filters.get('to_date')):
		condition += f""" AND jc.posting_date <= "{filters['to_date']}" """
	if filters.get('workstation'):
		condition += f""" AND jc.workstation = "{filters['workstation']}" """
	if filters.get('employee'):
		condition += f""" AND jct.employee = "{filters['employee']}" """
	if filters.get('item'):
		condition += f""" AND jc.production_item = "{filters['item']}" """

	query = f""" 
			SELECT 
				jc.name as job_card,
				jc.posting_date as date,
				jc.production_item as item_code,
				jc.workstation as workstation,
				jct.employee as employee,
				IFNULL(TIMESTAMPDIFF(MINUTE, jct.from_time, jct.to_time), 0)/60 as total_hrs,
				IFNULL(jct.completed_qty, 0) as actual_qty
			FROM
				`tabJob Card` jc left join `tabJob Card Time Log` jct
				on jc.name = jct.parent 
			WHERE
				{condition}
			ORDER BY
				jc.posting_date desc
			"""
	data = frappe.db.sql(query, as_dict=1)
	workstation_capacity = {}
	workstations = frappe.db.get_all('Workstation', pluck='name')
	for i in workstations:
		capacity = frappe.db.get_all('Workstation Capacity', filters={'parent':i}, fields=['item_code', 'production_capacity'])
		capacity = {i['item_code']:i['production_capacity'] for i in capacity}
		workstation_capacity[i] = capacity
	for row in data:
		row['expected_qty'] = row['total_hrs'] * workstation_capacity[row['workstation']].get(row['item_code'],0)
		row['effective_percent'] = round(row['actual_qty']/row['expected_qty'] *100, 2) if row['expected_qty'] else 0
	return data