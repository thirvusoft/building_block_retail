import frappe

@frappe.whitelist()
def balance_purchase_receipt(supplier):
    return frappe.db.sql(
        """select sum(pr.rounded_total*(100-pr.per_billed)/100) as balance
        from `tabPurchase Receipt` pr
        where pr.supplier = "{0}" and
        pr.docstatus =1
        group by pr.supplier
        """.format(supplier),as_dict=1)
