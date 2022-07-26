let tot_comp_qty = 0;
let opr = '';
let workstation = '';
let job_card_name = '';
frappe.ui.form.on("Job Card",{
    refresh: function(frm){
        job_card_name = frm.doc.name
        if(frm.doc.status != 'Completed' && frm.doc.status != 'Open')
        frm.add_custom_button("Finish",()=>{
            if(frm.doc.work_order){
                tot_comp_qty = frm.doc.total_completed_qty
                opr = frm.doc.operation
                workstation = frm.doc.workstation
            frappe.call({
                method:"building_block_retail.building_block_retail.custom.py.job_card.get_workorder_doc",
                args:{
                    work_order:frm.doc.work_order,
                    opr:frm.doc.operation,
                    workstation:frm.doc.workstation,
                    qty : frm.doc.total_completed_qty
                    },
                callback(r){
                    make_se(tot_comp_qty,r.message, "Manufacture", frm)
                }
            })
        }
        }).addClass("btn-warning").css({'color':'white','background-color': '#4CBB17','box-shadow': '2px 2px 2px #4CBB17'});
    },
    onload: function(frm){
        if(frm.doc.doc_onload == 0){
        frm.set_value('time_logs',[])
        frm.set_value('doc_onload',1)
        frm.refresh()
        frm.save()
        }
    },
    before_save: function(frm){
        frm.set_value('max_qty', frm.doc.for_quantity)
    }
})


function make_se (tot_comp_qty, frm, purpose, cur) {
    show_prompt_for_qty_input(frm, purpose)
        .then(data => {
            if(data.qty<=0){return}
            frappe.call({
                method: 'building_block_retail.building_block_retail.custom.py.job_card.update_operation_completed_qty',
                args:{work_order:frm.name,
                    opr,
                    workstation,
                    qty : tot_comp_qty
                    },
                callback(){
                    frappe.call({
                        method: 'erpnext.manufacturing.doctype.work_order.work_order.make_stock_entry', 
                        args:{
                        'work_order_id': frm.name,
                        'purpose': purpose,
                        'qty': (data.qty)
                        },
                        callback(r){
                            r.message.ts_job_card = cur.doc.name
                            frappe.model.sync(r.message);
                            frappe.set_route('Form', r.message.doctype, r.message.name);
                        }
                        });
                }
            })
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
        frappe.call({
            method:"building_block_retail.building_block_retail.custom.py.job_card.calculate_max_qty",
            async:false,
            args:{
                job_card:job_card_name,
                },
            callback(r){
                max = r.message
            }
        })
    } else {
        if (purpose === 'Manufacture') {
            max = flt(frm.material_transferred_for_manufacturing) - flt(frm.produced_qty);
        } else {
            max = flt(frm.qty) - flt(frm.material_transferred_for_manufacturing);
        }
    }
    return flt(max);
}