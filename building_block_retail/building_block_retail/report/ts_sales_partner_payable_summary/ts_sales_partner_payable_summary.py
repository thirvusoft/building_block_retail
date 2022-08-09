# Copyright (c) 2022, Thirvusoft and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data

def get_columns():
    return [
		{
			'fieldname':'sales_partner',
			'label':'Sales Partner',
			'fieldtype':'Link',
			'options':'Sales Partner',
   			'width': 200
		},
		{
			'fieldname':'amount_pending',
			'label':'Amount Pending',
			'fieldtype':'Currency',
			'width': 200
		},
  		{
			'fieldname':'partner_type',
			'label':'Partner Type',
			'fieldtype':'Link',
			'options':'Sales Partner Type',
   			'width': 200
		},
		{
			'fieldname':'territory',
			'label':'Territory',
			'fieldtype':'Link',
			'options':'Territory',
			'width': 200
		}
	]

def get_data(filters=None):
    filter={}
    if(filters.get('sales_partner')):filter['name'] = filters.get('sales_partner')
    if(filters.get('partner_type')):filter['partner_type'] = filters.get('partner_type')
    if(filters.get('territory')):filter['territory'] = filters.get('territory')
    sales_partner = frappe.get_all('Sales Partner', fields=['name', 'partner_type', 'commission_rate', 'territory'], filters=filter)
    
    report_data=[]
    for i in sales_partner:
        filter={}
        filter['sales_partner'] = i['name']
        sales_data = frappe.get_all('Sales Invoice', filters=filter, fields=['sales_partner', 'total_commission'])
        sales_partner = [j['sales_partner'] for j in sales_data]
        commission_amount = sum([k['total_commission'] for k in sales_data]) or 0
        payment_data = sum(frappe.get_all('Payment Entry', filters={'party_type':'Supplier', 'party':['in', sales_partner]}, pluck='paid_amount')) or 0
        report_data.append({'sales_partner':i['name'], 'amount_pending':commission_amount-payment_data, 'partner_type':i.get('partner_type'), 'territory':i.get('territory')})
    return report_data