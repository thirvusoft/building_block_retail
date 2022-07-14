frappe.ui.form.on("Job Card",{
    refresh: function(frm){
        frm.add_custom_button("Finish",()=>{
            if(frm.doc.work_order){
            frappe.call({
                method:"sgp.sgp.custom.py.job_card.get_workorder_doc",
                args:{
                    work_order:frm.doc.work_order,
                    opr:frm.doc.operation,
                    workstation:frm.doc.workstation,
                    qty : frm.doc.total_completed_qty
                    },
                callback(r){
                    make_se(r.message, "Manufacture")
                }
            })
        }
        })
    }
})
function make_se (frm, purpose) {
    show_prompt_for_qty_input(frm, purpose)
        .then(data => {
            return frappe.xcall('erpnext.manufacturing.doctype.work_order.work_order.make_stock_entry', {
                'work_order_id': frm.name,
                'purpose': purpose,
                'qty': data.qty
            });
        }).then(stock_entry => {
            frappe.model.sync(stock_entry);
            frappe.set_route('Form', stock_entry.doctype, stock_entry.name);
        });

}
function show_prompt_for_qty_input(frm, purpose) {
    let max = get_max_transferable_qty(frm, purpose);
    return new Promise((resolve, reject) => {
        frappe.prompt({
            fieldtype: 'Float',
            label: __('Qty for {0}', [purpose]),
            fieldname: 'qty',
            description: __('Max: {0}', [max]),
            default: max
        }, data => {
            max += (frm.qty * (frm.over_prdn_prcnt || 0.0)) / 100;

            if (data.qty > max) {
                frappe.msgprint(__('Quantity must not be more than {0}', [max]));
                reject();
            }
            if(data.qty > cur_frm.doc.total_completed_qty)
            data.purpose = purpose;
            resolve(data);
        }, __('Select Quantity'), __('Create'));
    });
}
function get_max_transferable_qty (frm, purpose){
    let max = 0;
    if (frm.skip_transfer) {
        max = flt(frm.qty) - flt(frm.produced_qty);
    } else {
        if (purpose === 'Manufacture') {
            max = flt(frm.material_transferred_for_manufacturing) - flt(frm.produced_qty);
        } else {
            max = flt(frm.qty) - flt(frm.material_transferred_for_manufacturing);
        }
    }
    return flt(max);
}