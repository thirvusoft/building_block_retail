import frappe

def execute():
    jee = frappe.db.sql("""
        select
            jea.parent,
            (select je.posting_date from `tabJournal Entry` je where je.name = jea.parent) as date   
        from `tabJournal Entry Account` jea
        where
            jea.docstatus = 1 and
            jea.debit > 0 and
            (select acc.account_type from `tabAccount` acc where acc.name = jea.account ) in ('Cash', 'Bank')
        group by jea.parent
        order by (select je.posting_date from `tabJournal Entry` je where je.name = jea.parent)
    """, as_dict=True)

    for i in jee:
        print(i.parent)
        je = frappe.get_doc('Journal Entry', i.parent)
        for row in je.accounts:
            row.debit, row.credit = row.credit, row.debit
            row.debit_in_account_currency, row.credit_in_account_currency = row.credit_in_account_currency, row.debit_in_account_currency

            row.db_set('debit', row.debit)
            row.db_set('credit', row.credit)
            row.db_set('debit_in_account_currency', row.debit_in_account_currency)
            row.db_set('credit_in_account_currency', row.credit_in_account_currency)
        
        je.docstauts = 2
        je.make_gl_entries(1)

        je.docstatus = 1
        je.ignore_linked_doctypes = ('GL Entry', 'Stock Ledger Entry')
        je.make_gl_entries()