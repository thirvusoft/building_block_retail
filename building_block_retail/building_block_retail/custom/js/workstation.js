frappe.ui.form.on("Workstation", {
    setup: function(frm){
        let items = [];
        frm.doc.item_wise_production_capacity.forEach(d=>{
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
    }
})

frappe.ui.form.on("Workstation Capacity", {
    item_code: function(frm){
        let items = [];
        frm.doc.item_wise_production_capacity.forEach(d=>{
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