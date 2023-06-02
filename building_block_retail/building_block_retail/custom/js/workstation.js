frappe.ui.form.on("Workstation", {
    setup: function(frm){
        let items = [];
        (frm.doc.item_wise_production_capacity || []).forEach(d=>{
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
    get_items: async function (frm) {
        frappe.call({
            method:"building_block_retail.building_block_retail.custom.py.item.item_list",
            callback: function(r){
                r.message.forEach((data)=>{
                    var Workstation = frm.add_child("item_wise_production_capacity")
                    Workstation.item_code = data["item_code"]
                   
                })
                frm.refresh_field("item_wise_production_capacity")
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
        (frm.doc.item_wise_production_capacity  || []).forEach(d=>{
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