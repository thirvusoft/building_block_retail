frappe.ui.form.on('TS Supplier Default Items', 'before_default_items_remove', function(frm, cdt, cdn){
        let p = locals[cdt][cdn]
        // frappe.db.get_list("Item Supplier",{filters:{'parent':p.item,'parentfield': 'supplier_items','parenttype' : 'Item','supplier' : p.parent}, fields:['name']}).then((data)=>{
        //     frappe.db.delete_doc('Item Supplier', data[0].name)
        // })
        frappe.call({
            method: 'sgp.sgp.custom.py.supplier.remove_default_supplier_from_items',
            args:{doc:p},
            freeze:true,
            freeze_message: 'Please Wait deleting suppliers from Item......',
            callback(r){
                cur_frm.refresh()
            }
        })
    }
)


frappe.ui.form.on("Supplier",{
    refresh: function(frm){
        frappe.call({
            method: 'sgp.sgp.custom.py.supplier.add_supplier_to_default_supplier_in_item',
            args:{doc:frm.doc},
        })
    },
    remove_items: function(frm){
        frappe.confirm(
            'Are you sure want to delete all linked default supplier items?',
            // function(){
            //     window.close();
            // },
            function(){
                frappe.call({
                    method: 'sgp.sgp.custom.py.supplier.remove_default_supplier_from_items',
                    args:{doc:frm.doc.default_items},
                    freeze:true,
                    freeze_message: 'Please Wait deleting suppliers from Item......',
                    async:false,
                    callback(){
                        cur_frm.set_value('default_items',[])
                        // cur_frm.refresh()
                        cur_frm.save()
                        show_alert('Deleted all Links.')
                    }
                })
            }
        )
    }
})