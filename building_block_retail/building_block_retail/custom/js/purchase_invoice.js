frappe.ui.form.on("Purchase Invoice",{
    refresh: async function(frm){
        let items_list = [];
        if(frm.doc.items){
            frm.doc.items.forEach((row)=>{
                if(row.item_group == 'Fuel'){
                    items_list.push(row)
                }
            })
        }
        if(items_list.length ){
            frm.add_custom_button('Make Vehicle Log', async ()=>{
                let fields = [], vehicles = [];
                frm.doc.items.forEach((row)=>{
                    if(!vehicles.includes(row.vehicle) && row.item_group == 'Fuel'){
                        vehicles.push(row.vehicle)
                    }
                })
                let i =0;
                for(let vl of vehicles){
                    fields.push({'fieldtype':'Link', 'options':'Vehicle', 'label':'Vehcile', 'read_only':1, 'fieldname':`vehicle${i}`, 'default':vl})
                    fields.push({'fieldtype':'Column Break'})
                    fields.push({'fieldtype':'Float', 'label':'Current Odometer After trip', 'fieldname':`odd${i}`, 'default':(await frappe.db.get_value('Vehicle', vl, 'last_odometer')).message.last_odometer})
                    fields.push({'fieldtype':'Column Break'})
                    fields.push({'fieldtype':'Link', 'options':'Employee', 'label':'Employee(Driver)', 'reqd':1, 'filters':{'designation':'Driver'}, 'fieldname':`employee${i}`})
                    fields.push({'fieldtype':'Section Break'})
                    i+=1;
                }
               
                let dialog = new frappe.ui.Dialog({
                    title:'Select Driver and Current Odometer Value',
                    size: 'large',
                    fields:fields,
                    primary_action(data){
                        dialog.hide()
                        frappe.call({
                            method:'building_block_retail.building_block_retail.custom.py.purchase_invoice.make_vehicle_log',
                            args:{
                                doc: frm.doc,
                                data:data,
                                vehicles:vehicles
                            },
                            freeze:true,
                            freeze_message:`
        
                            <div class="main">
                              <div class="spinner">
                                <div class="bubble-1"></div>
                                <div class="bubble-2"></div>
                              </div>
                            
                            </div>
                            
                            `,
                            callback(r){
                            }
                        })
                    }
                })
                dialog.show()
                let labels = dialog.$wrapper.find('.control-label')
                for(let i=0;i<labels.length;i++){
                    labels[i].style.fontWeight = 'bold'
                }
            }).css('background-color', '#e2f2ac')
        }
    },
    //  Thirvu_dual_Accounting
    company:function(frm){
        if(frm.doc.company){
        frappe.call({
            method:"building_block_retail.building_block_retail.custom.py.sales_order.branch_list",
            args:{
                company:frm.doc.company
            },
            callback: function(r){
               
            frm.set_query('branch',function(frm){
                return{
                    filters:{
                        'name':['in',r.message]
                    }
                }
            
            })
            }
        })}},
    taxes_and_charges: function(frm) {
        if(frm.doc.branch) {
            frappe.db.get_value("Branch", frm.doc.branch, "is_accounting").then( value => {
                if (!value.message.is_accounting) {
                    if(frm.doc.taxes_and_charges)
                        frm.set_value("taxes_and_charges", "")
                    if(frm.doc.tax_category)
                        frm.set_value("tax_category", "")
                    if(frm.doc.taxes)
                        frm.clear_table("taxes")
                        refresh_field("taxes")
                }
            })
        }
    },
    tax_category: function(frm) {
        frm.trigger("taxes_and_charges")
    },
    branch: function (frm) {
        frm.trigger("taxes_and_charges")
    },
    validate: function(frm) {
        frm.trigger("taxes_and_charges")
    }
})