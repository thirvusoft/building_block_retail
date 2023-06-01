let tot_comp_qty = 0;
let opr = '';
let workstation = '';
let job_card_name = '';
frappe.ui.form.on("Job Card",{
    refresh: function(frm){
        frm.set_df_property('operation_row_number', 'hidden', 1)
        job_card_name = frm.doc.name
        if(!frm.is_new() && !([1,2],frm.doc.docstatus)){
        if(!frm.is_dirty()){
            frm.page.btn_primary[0].innerHTML  = '<span class="alt-underline">F</span>inish'
        }
        
    }
        frm.set_query('employee','time_logs', function() {
            return {
                filters: {
                    'Designation': "Contractor"
                }
            }
        });
        frm.set_query('employee', function() {
            return {
                filters: {
                    'Designation': "Contractor"
                }
            }
        });

        frm.set_query('source_warehouse', ()=>{
            return {
                filters:{
                    'is_group':0,
                    'disabled':0,
                    'company':frm.doc.company
                }
            }
        })
        frm.set_query('target_warehouse', ()=>{
            return {
                filters:{
                    'is_group':0,
                    'disabled':0,
                    'company':frm.doc.company
                }
            }
        })
        if(frm.doc.docstatus == 1){
            frappe.db.get_value("Stock Entry", {"ts_job_card":frm.doc.name, "docstatus":["!=", 2]}, "name").then(
                (r)=>{
                    if(!r.message.name){
                        frm.add_custom_button("Make Stock Entry", ()=>{
                            frappe.call({
                                method: "building_block_retail.building_block_retail.custom.py.job_card.make_stock_entry",
                                args: {
                                    job_card: frm.doc.name,
                                    qty: frm.doc.total_completed_qty,
                                    purpose: "Manufacture"
                                },
                                callback(r){
                                    if(r.message){
                                        frappe.show_alert(`Stock Entry Created ${r.message}`);
                                        frm.remove_custom_button("Make Stock Entry")
                                        frm.refresh()
                                    }
                                }
                            })
                        })
                    }
                }
            )
        }
        
    },
    onload: function(frm){
        if(frm.doc.doc_onload == 0 && frm.is_new()){
        frm.set_value('time_logs',[])
        frm.set_value('doc_onload',1)
        frm.refresh()
        // frm.save()
        }
    },
    before_save: function(frm){
        frm.set_value('max_qty', frm.doc.for_quantity)
    },
    toggle_operation_number(frm) {
		frm.toggle_display("operation_row_number", !frm.doc.operation_id && frm.doc.operation);
	}
})