frappe.ui.form.on(cur_frm.doc.doctype, {
    set_inclusive_tax: function(frm, cdt, cdn) {
        if (frm.doc.taxes) {
            for (var i = 0; i < frm.doc.taxes.length; i++) {
                frappe.model.set_value(frm.doc.taxes[i].doctype, frm.doc.taxes[i].name, 'included_in_print_rate', frm.doc.set_inclusive_tax );
            }
        }
    }
})