frappe.ui.form.on("Purchase Receipt" ,{
    onload:function(frm){
        
        let tax_field = 'taxes_and_charges_in_landed'
        frm.set_query("expense_account", tax_field, function() {
            return {
                filters: {
                    "account_type": ['in', ["Tax", "Chargeable", "Income Account", "Expenses Included In Valuation", "Expenses Included In Asset Valuation"]],
                    "company": frm.doc.company
                }
            };
        })
        frm.set_query('transporter', function(frm){
                    return {
                        filters:{
                            'supplier_name': 'Own Transporter'
                        }
                    }
                });
        // To ignore price list while changing conversion factor
        frappe.flags.dont_fetch_price_list_rate = true
        },
    taxes_and_charges: function(frm) {
        if(frm.doc.branch && frm.doc.docstatus != 1) {
            frappe.db.get_value("Branch", frm.doc.branch, "is_accounting").then( value => {
                if (!value.message.is_accounting) {
                    if(frm.doc.taxes_and_charges)
                        frm.set_value("taxes_and_charges", "")
                    if(frm.doc.tax_category)
                        frm.set_value("tax_category", "")
                    if(frm.doc.taxes)
                        frm.clear_table("taxes")
                        refresh_field("taxes")
                }
            })
        }
    },
    tax_category: function(frm) {
        frm.trigger("taxes_and_charges")
    },
    branch: function (frm) {
        frm.trigger("taxes_and_charges")
    },
    validate: function(frm) {
        frm.trigger("taxes_and_charges")
    },

        // Thirvu_dual_Accounting
        company:function(frm){
            if(frm.doc.company){
            frappe.call({
                method:"building_block_retail.building_block_retail.custom.py.sales_order.branch_list",
                args:{
                    company:frm.doc.company
                },
                callback: function(r){
                   
                frm.set_query('branch',function(frm){
                    return{
                        filters:{
                            'name':['in',r.message]
                        }
                    }
                
                })
                }
            })}}
})

frappe.ui.form.on('Landed Cost Taxes and Charges', {
	expense_account: function(frm, cdt, cdn) {
		set_account_currency(frm, cdt, cdn);
	},

	amount: function(frm, cdt, cdn) {
		set_base_amount(frm, cdt, cdn);
	},
});
function set_account_currency (frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    if (row.expense_account) {
        frappe.db.get_value('Account', row.expense_account, 'account_currency', function(value) {
            frappe.model.set_value(cdt, cdn, "account_currency", value.account_currency);
            set_exchange_rate(frm, cdt, cdn);
        });
    }
}

function set_exchange_rate(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    let company_currency = frappe.get_doc(":Company", frm.doc.company).default_currency;

    if (row.account_currency == company_currency) {
        row.exchange_rate = 1;
        frm.set_df_property('taxes_and_charges_in_landed', 'hidden', 1, row.name, 'exchange_rate');
    } else if (!row.exchange_rate || row.exchange_rate == 1) {
        frm.set_df_property('taxes_and_charges_in_landed', 'hidden', 0, row.name, 'exchange_rate');
        frappe.call({
            method: "erpnext.accounts.doctype.journal_entry.journal_entry.get_exchange_rate",
            args: {
                posting_date: frm.doc.posting_date,
                account: row.expense_account,
                account_currency: row.account_currency,
                company: frm.doc.company
            },
            callback: function(r) {
                if (r.message) {
                    frappe.model.set_value(cdt, cdn, "exchange_rate", r.message);
                }
            }
        });
    }

    frm.refresh_field('taxes_and_charges_in_landed');
}

function set_base_amount(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    frappe.model.set_value(cdt, cdn, "base_amount",
        flt(flt(row.amount)*row.exchange_rate, precision("base_amount", row)));
    total_taxes_and_charges(frm, cdt, cdn)
}
function total_taxes_and_charges(frm, cdt, cdn){
    var total =0
    for(var i=0;i<frm.doc.taxes_and_charges_in_landed.length;i++){
        total += frm.doc.taxes_and_charges_in_landed[i].base_amount
    }
    frm.set_value("total_taxes_and_charges_in_landed",total)
}