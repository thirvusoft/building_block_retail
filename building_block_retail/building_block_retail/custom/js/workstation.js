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
    get_items: async function (frm,cdt,cdn) {
        let items = [];
        (frm.doc.item_wise_production_capacity  || []).forEach(d=>{
            items.push(d.item_code)
        })
        let temp_items = [];
        (frm.doc.item_template  || []).forEach(d=>{
            temp_items.push(d.template)
        })
    
        frappe.call({
            method:"building_block_retail.building_block_retail.custom.py.workstation.item_list",
            args:{items:items,
            template:temp_items},
            callback: function(r){
              
               if(r.message.length<3){
                frm.set_df_property('item_template', 'hidden', 0);
                   
                r.message[0].forEach(value=>
                 
                    {
                    var template_tab=frm.add_child("item_template")
                    template_tab.template=value["item_code"]
                    })
                     r.message[1].forEach(value=>
                 
                        {
                    var variant_tab=frm.add_child("item_wise_production_capacity")
                    variant_tab.item_code=value["item_code"]
                    variant_tab.variant_of=value["variant_of"]
                   
                        })
                        
                     frm.refresh_field("item_template")
                     frm.refresh_field("item_wise_production_capacity")
               }
               else{
                frm.set_df_property('item_template', 'hidden', 1);
                r.message.forEach(value=>
                    {
                        var Workstation=frm.add_child("item_wise_production_capacity")
                        Workstation.item_code=value["item_code"]
                        Workstation.variant_of=value["variant_of"]
                    })
                    frm.refresh_field("item_wise_production_capacity")

               }
                
               
            }
        })
        frm.refresh_field("item_wise_production_capacity")
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