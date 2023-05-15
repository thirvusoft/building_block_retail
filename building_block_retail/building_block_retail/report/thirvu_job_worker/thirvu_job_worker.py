# Copyright (c) 2022, Thirvusoft and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    get_data(filters)
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    employee = filters.get("employee")
    site_name = filters.get("site_name")
    conditions = ""
    adv_conditions = ""
    if from_date or to_date or employee or site_name:
        conditions = " where 1 = 1"
        adv_conditions = "where 1 = 1"
        if from_date and to_date:
            conditions += "  and jwd.start_date between '{0}' and '{1}' ".format(from_date, to_date)
            adv_conditions += " and empadv.posting_date between '{0}' and '{1}' ".format(from_date, to_date)
        if employee:
            conditions += " and jwd.name1 ='{0}' ".format(employee)
        if site_name:
            conditions += " and site.name = '{0}' ".format(site_name)
    report_data = frappe.db.sql(""" select *,(amount + salary_balance - advance_amount) from (select (select employee_name from `tabEmployee` where name = jwd.name1 ) as jobworker,site.name,site.status,jwd.sqft_allocated,
                                        emp.salary_balance as salary_balance,jwd.amount as amount,
                                        (select sum(empadv.advance_amount - empadv.return_amount) from `tabEmployee Advance` as empadv {1} and empadv.employee = jwd.name1 and docstatus = 1) as advance_amount
                                        from `tabProject` as site
                                        left outer join `tabTS Job Worker Details` as jwd
                                            on site.name = jwd.parent
                                        left outer join `tabEmployee` as emp
                                            on emp.employee = jwd.name1
                                        {0}
                                    group by jwd.name1,jwd.sqft_allocated)as total_cal
                                """.format(conditions,adv_conditions))
    data = [list(i) for i in report_data]
    final_data = []
    c = 0
    if(len(data)):
        start = 0
        for i in range(len(data)-1):
            if (data[i][0] != data[i+1][0]):
                adv=data[i][6]
                data[i][6]=[]
                final_data.append(data[i])
                total = [" " for i in range(8)]
                total[2] = "<b style=color:orange;>""Total""</b>"
                total[3] = sum(data[i][3]or 0 for i in range(start,i+1))
                total[4] = sum(data[i][4]or 0 for i in range(start,i+1))
                total[5] = sum(data[i][5]or 0 for i in range(start,i+1))
                total[6] = adv
                total[7] = sum(data[i][7]or 0 for i in range(start,i+1))
                final_data.append(total)
                start = i+1	
                c=0
            else:
                if(c==0):data[i][6]=()
                else:data[i][6]=()
                c+=1
                final_data.append(data[i])
        adv=data[-1][6]
        data[-1][6]=()      
        final_data.append(data[-1])
        total = [" " for i in range(8)]
        total[2] = "<b style=color:orange;>""Total""</b>"
        total[3] = sum(data[i][3]or 0 for i in range(start,len(data)))
        total[4] = sum(data[i][4]or 0 for i in range(start,len(data)))
        total[5] = sum(data[i][5]or 0 for i in range(start,len(data)))
        total[6] = adv
        total[7] = sum(data[i][7]or 0 for i in range(start,len(data)))
        final_data.append(total)
    columns = get_columns()
    return columns, get_data(filters)

def get_columns():
    columns = [
        _("Job Worker") + ":Data/Employee:150",
        _("Site Name") + ":Link/Project:150",
        _("Status") + ":Data/Project:150",
        _("Completed Sqft") + ":Data:150",
        _("Salary Balance") + ":Currency:150",
        _("Amount") + ":Currency:150",
        # _("Advance Amount") + ":Currency:150",
        _("Total Amount") + ":Currency:150",
        ]
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
        # {
        #     'fieldname':'',
        #     'label':'Job Worker',
        #     'fieldtype':'Link',
        #     'options':'Employee'
        # },

    ]
    return columns


# frappe.db.sql("""select sum(empadv.advance_amount - empadv.return_amount) from `tabEmployee Advance` as empadv where empadv.employee = '{0}' and docstatus = 1""".format(data[i+0][0]))


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