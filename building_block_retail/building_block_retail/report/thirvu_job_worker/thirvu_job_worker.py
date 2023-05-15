# Copyright (c) 2022, Thirvusoft and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    data = get_data(filters)
    columns = get_columns()

    return columns, data

def get_columns():
    columns = [
        {
            'fieldname':'job_worker',
            'label':'Job Worker',
            'fieldtype':'Data',
            'width':150
        },
        {
            'fieldname':'site_name',
            'label':'Site Name',
            'fieldtype':'Link',
            'options':'Project',
            'width':300
        },
        {
            'fieldname':'status',
            'label':'Status',
            'fieldtype':'Data',
            'width':150
        },
        {
            'fieldname':'sqft_allocated',
            'label':'Completed Sqft',
            'fieldtype':'Float',
            'width':150
        },
      
        {
            'fieldname':'amount',
            'label':'Amount',
            'fieldtype':'Currency',
            'width':150
        },
          {
            'fieldname':'salary_balance',
            'label':'Salary Balance',
            'fieldtype':'Currency',
            'width':150
        },
    ]
    return columns



def get_data(filters= {}):
    final_data = []
    condition = " 1 = 1 "
    jw_filter = {}
    if(filters.get('from_date') and filters.get('to_date')):
        jw_filter['date'] = ['between', (filters.get('from_date'), filters.get('to_date'))]
    elif(filters.get('from_date')):
        jw_filter['date'] = [ ">=", filters.get('from_date')]
    elif(filters.get('to_date')):
        jw_filter['date'] = [ "<=", filters.get('to_date')]
    
    if(filters.get('employee')):
        jw_filter['name1'] = filters.get('employee')
    if(filters.get('site_name')):
        jw_filter['parent'] = filters.get('site_name')

    
    data = frappe.db.get_all("Finalised Job Worker Details", filters=jw_filter, fields = ['name1 as employee', 'date', 'parent as site_name', 'sum(sqft_allocated) as sqft_allocated', 'sum(amount) as amount'], group_by = "name1, parent", order_by = "name1")
    sqft, amt, sal_bal = 0,0,0
    for i in range(len(data)):
        data[i]['job_worker'] = frappe.db.get_value('Employee', data[i]['employee'], 'employee_name')
        data[i]['status'] = frappe.db.get_value('Project', data[i]['site_name'], 'status')
        data[i]['salary_balance'] = data[i]['amount'] - (frappe.db.sql(f"""
        select sum(paid_amount) from `tabSite work Details` swd left outer join `tabSalary Slip` ss on ss.name = swd.parent where swd.site_work_name = "{data[i]['site_name']}" and ss.employee = "{data[i]['job_worker']}" 
        """, as_list=1)[0][0] or 0)
        final_data.append(data[i])
        sqft += data[i]['sqft_allocated']
        amt += data[i]['amount']
        sal_bal += data[i]['salary_balance']
        if(i<(len(data)-1)):
            if(data[i]['employee'] != data[i+1]['employee']):
                final_data.append({'status':'Total', 'sqft_allocated':sqft, 'amount':amt, 'salary_balance':sal_bal})
                sqft, amt, sal_bal = 0,0,0
    if(len(data)):
        final_data.append({'status':'Total', 'sqft_allocated':sqft, 'amount':amt, 'salary_balance':sal_bal})
    return final_data