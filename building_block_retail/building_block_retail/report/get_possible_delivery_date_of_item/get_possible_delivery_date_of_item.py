# Copyright (c) 2022, Thirvusoft and contributors
# For license information, please see license.txt

import json
import frappe
import datetime


def execute(filters={}):
	columns = get_columns() or []
	data, possible_date, max_qty, holiday_list, actual_stock = get_data(filters) or ([],'', 0, '', 0)
	summary = [
		{
			"value": possible_date,
			"indicator": "Blue",
			"label": "Possible Delivery Date",
			"datatype": "Date",
		},
		{
			"value": max_qty,
			"indicator": "green",
			"label": "Per day Production Limit",
			"datatype": "Data",
		},
		{
			"value": actual_stock,
			"indicator": "red",
			"label": "Actual Qty",
			"datatype": "Data",
		}
	]
	return columns, data, f'Exclude Holidays metioned in <b>{holiday_list}</b><br>Enter qty in Pieces', None, summary


def get_columns():
	columns=[
		{
			'fieldname':'sales_order',
			'label':'Sales Order',
			'fieldtype':'Link',
			'options':'Sales Order'
		},
		{
			'fieldname':'work_order',
			'label':'Work Order',
			'fieldtype':'Link',
			'options':'Work Order'
		},
		{
			'fieldname':'qty',
			'label':'Ordered Qty',
			'fieldtype':'Float',
		},
		{
			'fieldname':'prod_qty',
			'label':'Produced Qty',
			'fieldtype':'Float',
		},
		{
			'fieldname':'possible_date_of_completion',
			'label':'Possible date of completion',
			'fieldtype':'Date',
		},
	]

	return columns


def date_by_adding_business_days(from_date, add_days, leave_days=[]):
    business_days_to_add = add_days
    current_date = from_date
    while business_days_to_add > 0:
        current_date += datetime.timedelta(days=1)
        weekday = current_date.weekday()
        if weekday in leave_days: 
            continue
        business_days_to_add -= 1
    return current_date

#demo:
# print '10 business days from today:'
# print date_by_adding_business_days(datetime.date.today(), 10)

@frappe.whitelist()
def get_data(filters, call_from_report = 1, check_warehouse=[]):
	if(isinstance(filters, str)):
		filters = json.loads(filters)
		call_from_report = int(call_from_report)

	if(not filters.get('item_code')):
		frappe.msgprint('Select Item')
		return 
	max_qty = frappe.db.get_value('Item', filters['item_code'], 'daily_max_production_limit')
	def_holiday = frappe.db.get_all('Holiday List', pluck='name')
	if(not len(def_holiday)):
		frappe.msgprint('Not able to find holiday list')
		return
	holiday = frappe.get_doc('Holiday List', def_holiday[0])
	weekdays = {'Monday':0, 'Tuesday':1, 'Wednesday':2, 'Thursday':3, 'Friday':4, 'Saturday':5, 'Sunday':6}
	leave_days = list(set([weekdays[i.description] for i in holiday.holidays]))
	if(not max_qty):
		frappe.msgprint(f'Enter Daily maximum production qty in Item <b>{filters["item_code"]}</b>')
		return
	bin_filt = {'item_code':filters['item_code']}
	if(len(check_warehouse)):
		bin_filt['warehouse'] = ['in', check_warehouse]
	actual_stock = sum(frappe.db.get_all('Bin', filters=bin_filt, pluck='actual_qty'))
	wo = frappe.db.get_all('Work Order', filters={'production_item':filters['item_code'], 'docstatus':['!=', 2], 'priority':['!=', 'Low Priority']}, fields=['name', 'sales_order', 'qty', 'produced_qty'])
	tot_qty = sum([i['qty'] for i in wo])
	prod_qty = actual_stock
	days_count = (tot_qty + (filters.get('order_qty') or 0) - prod_qty)/max_qty
	possible_date = date_by_adding_business_days(datetime.date.today(), days_count, leave_days)

	if( not call_from_report):
		return possible_date
		
	data = []
	qty = 0
	for i in wo:
		qty += (i['qty'] - i['produced_qty'])
		days = qty/max_qty
		data.append({
			'sales_order':i['sales_order'],
			'work_order':i['name'],
			'qty':i['qty'],
			'prod_qty':i['produced_qty'],
			'possible_date_of_completion': date_by_adding_business_days(datetime.date.today(), days, leave_days)
		})
	return data, possible_date, max_qty, def_holiday[0], actual_stock