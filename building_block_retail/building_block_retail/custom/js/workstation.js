frappe.ui.form.on("Workstation", {
    setup: function(frm){
        let items = [];
        (frm.doc.item_wise_production_capacity||[]).forEach(d=>{
            items.push(d.item_code)
        })
        frm.set_query('item_code', 'item_wise_production_capacity', function(frm){
            return {
                filters:{
                    'name':['not in', items]
                }
            }
        })
    },
    refresh:function(frm){
        frm.trigger('setup')
        frm.set_query('source_warehouse', ()=>{
            return {
                filters:{
                    'is_group':0,
                    'disabled':0,
                }
            }
        })
        frm.set_query('target_warehouse', ()=>{
            return {
                filters:{
                    'is_group':0,
                    'disabled':0,
                }
            }
        })
    }
})

frappe.ui.form.on("Workstation Capacity", {
    item_code: function(frm){
        let items = [];
        (frm.doc.item_wise_production_capacity||[]).forEach(d=>{
            items.push(d.item_code)
        })
        frm.set_query('item_code', 'item_wise_production_capacity', function(frm){
            return {
                filters:{
                    'name':['not in', items]
                }
            }
        })
    }
})