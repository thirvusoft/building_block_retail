frappe.provide('vb');
frappe.ui.form.on('Sales Order', {
    refresh: function (frm) {
        vb.showCustomerPaymentInfo({ 'customer': frm.doc.customer, 'company': frm.doc.company });
    },
    customer: function (frm) {
        vb.showCustomerPaymentInfo({ 'customer': frm.doc.customer, 'company': frm.doc.company });
    },
    company: function (frm) {
        vb.showCustomerPaymentInfo({ 'customer': frm.doc.customer, 'company': frm.doc.company });
    }
});

frappe.ui.form.on('Sales Invoice', {
    refresh: function (frm) {
        vb.showCustomerPaymentInfo({ 'customer': frm.doc.customer, 'company': frm.doc.company });
    },
    customer: function (frm) {
        vb.showCustomerPaymentInfo({ 'customer': frm.doc.customer, 'company': frm.doc.company });
    },
    company: function (frm) {
        vb.showCustomerPaymentInfo({ 'customer': frm.doc.customer, 'company': frm.doc.company });
    }
});

frappe.ui.form.on('Quotation', {
    refresh: function (frm) {
        frm.doc.quotation_to == "Customer" ? vb.showCustomerPaymentInfo({ 'customer': frm.doc.party_name, 'company': frm.doc.company }) : cur_frm.dashboard.clear_comment();
    },
    party_name: function (frm) {
        frm.doc.quotation_to == "Customer" ? vb.showCustomerPaymentInfo({ 'customer': frm.doc.party_name, 'company': frm.doc.company }) : cur_frm.dashboard.clear_comment();
    },
    company: function (frm) {
        frm.doc.quotation_to == "Customer" ? vb.showCustomerPaymentInfo({ 'customer': frm.doc.party_name, 'company': frm.doc.company }) : cur_frm.dashboard.clear_comment();
    }
});

vb.showCustomerPaymentInfo = async function ({ customer, company }) {
    if (!customer || !company) {
        return;
    }
    cur_frm.dashboard.clear_comment();
    await frappe.call({
        method: "building_block_retail.building_block_retail.custom.py.customer.customer_outstanding_amount",
        args: {
            company: company,
            customer: customer
        },
        callback(r) {
            if (r.message) {
                cur_frm.dashboard.add_comment(`
                    <div><a href='/app/customer/${customer}'><b>${customer}</b></a><div>
                    <div><b>Total Unpaid Amount: ${r.message}</b></div>
                `, 'blue', true);
            }
        }
    });
}
