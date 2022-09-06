frappe.ui.form.on('Sales Invoice Item', {
    ts_qty: function(frm,cdt,cdn){
        bundle_calc(frm, cdt, cdn)
    },
    conversion_factor: function(frm,cdt,cdn){
        bundle_calc(frm, cdt, cdn)
    },
    pieces: function(frm,cdt,cdn){
        bundle_calc(frm, cdt, cdn)
    },
    qty: function(frm, cdt,cdn){
        var p = locals[cdt][cdn]
        if(p.item_code){
            frm.doc.items.forEach((item)=>{
                if(item.sales_order){
                    frm.doc.job_worker_table.forEach((row)=>{
                        if(row.item_code === item.item_code){
                            frappe.model.set_value(row.doctype, row.name, 'sqft', item.qty)
                        }
                    })
                    frm.refresh()
                }
            }) 
        }
    }
})


async function bundle_calc(frm, cdt, cdn){
    let row = locals[cdt][cdn]
    let uom=row.uom
    let conv1
    let conv2
    await frappe.db.get_doc('Item', row.item_code).then((doc) => {
        let bundle_conv=1
        let other_conv=1;
        let nos_conv=1
        for(let doc_row=0; doc_row<doc.uoms.length; doc_row++){
            if(doc.uoms[doc_row].uom==uom){
                other_conv=doc.uoms[doc_row].conversion_factor
            }
            if(doc.uoms[doc_row].uom=='bundle'){
                bundle_conv=doc.uoms[doc_row].conversion_factor
            }
            if(doc.uoms[doc_row].uom=='Nos'){
                nos_conv=doc.uoms[doc_row].conversion_factor
            }
        }
        conv1=bundle_conv/other_conv
        conv2=nos_conv/other_conv
    })

    if(row.item_group.indexOf('Paver')>=0 || row.item_group.indexOf('paver')>=0){
        frappe.model.set_value(cdt, cdn, 'qty', row.ts_qty*conv1 + row.pieces*conv2)
        let rate=row.rate
        frappe.model.set_value(cdt, cdn, 'rate', 0)
        frappe.model.set_value(cdt, cdn, 'rate', rate)
    }
    
}



frappe.ui.form.on('Sales Invoice', {
    onload:async function(frm){
        if(cur_frm.is_new() ){
            for(let ind=0;ind<cur_frm.doc.items.length;ind++){
                let cdt=cur_frm.doc.items[ind].doctype
                let cdn=cur_frm.doc.items[ind].name
                let row=locals[cdt][cdn]
                let uom=row.uom
                let conv1
                let conv2
                if(row.item_code)
                {
                    await frappe.db.get_doc('Item', row.item_code).then((doc) => {
                        let bundle_conv=1
                        let other_conv=1;
                        let nos_conv=1
                        for(let doc_row=0; doc_row<doc.uoms.length; doc_row++){
                            if(doc.uoms[doc_row].uom==uom){
                                other_conv=doc.uoms[doc_row].conversion_factor
                            }
                            if(doc.uoms[doc_row].uom=='bundle'){
                                bundle_conv=doc.uoms[doc_row].conversion_factor
                            }
                            if(doc.uoms[doc_row].uom=='Nos'){
                                nos_conv=doc.uoms[doc_row].conversion_factor
                            }
                        }
                        conv1=bundle_conv/other_conv
                        conv2=nos_conv/other_conv
                    })
            
                
               
                if(row.item_group.indexOf('Paver')>=0 || row.item_group.indexOf('paver')>=0){
                    let total_qty=row.qty
                    await frappe.model.set_value(cdt, cdn, 'ts_qty', parseInt(row.qty/conv1))
                    await frappe.model.set_value(cdt, cdn, 'pieces', 0)
                    let bundle_qty=row.qty
                    let pieces_qty=total_qty-bundle_qty
                    await frappe.model.set_value(cdt, cdn, 'pieces', pieces_qty/conv2)
                    let rate=row.rate
                    frappe.model.set_value(cdt, cdn, 'rate', 0)
                    frappe.model.set_value(cdt, cdn, 'rate', rate)
                }    
                }
            }
            let items = cur_frm.doc.items || [];
            let len = items.length;
            while (len--)
            {
                if(items[len].qty == 0)
                {
                    await cur_frm.get_field("items").grid.grid_rows[len].remove();
                }
            }
            cur_frm.refresh();
            var t_amt = 0;
            if(frm.doc.items){
                if(frm.doc.job_worker_table){
                    if(!frm.doc.job_worker_table.length){
                frm.doc.items.forEach((item)=>{
                    if(item.sales_order){
                        frappe.db.get_value("Sales Order",{'name':item.sales_order},"work").then((work)=>{
                            if(work.message.work === "Supply and Laying")
                            {
                                frappe.db.get_value('Item', {'item_code':item.item_code}, 'laying_cost').then((data)=>{
                                    if(item.item_group != "Raw Material"){
                                    var new_row = frm.add_child("job_worker_table");
                                    frappe.model.set_value(new_row.doctype,new_row.name,"item_code",item.item_code)
                                    frappe.model.set_value(new_row.doctype,new_row.name,"sqft",item.qty)
                                    frappe.model.set_value(new_row.doctype,new_row.name,"ratesqft",data.message.laying_cost)
                                    frappe.model.set_value(new_row.doctype,new_row.name,"ts_amount",item.qty * data.message.laying_cost)
                                    t_amt+=(item.qty * data.message.laying_cost)
                                    cur_frm.set_value("total_amount_job_worker",t_amt)
                                    }
                    
                                })
                            }
                        })
                        
                    }
                })       
            }}
            }

         
            
            }
            setTimeout(() => {
				frm.remove_custom_button('Fetch Timesheet');
				frm.remove_custom_button('E-Way Bill JSON', "Create");
				frm.remove_custom_button('Maintenance Schedule', "Create");
				frm.remove_custom_button('Subscription', "Create");
                frm.remove_custom_button('Invoice Discounting', "Create");
                frm.remove_custom_button('Dunning', "Create");
			}, 500); 
            cur_frm.set_query("jobworker_name",function(frm){
                return {
                    filters: {
                        "designation":"Job Worker",
                        "company":cur_frm.doc.company,
                        "status":"Active"
                    }
                }
            })
        },
        
        refresh:function(frm){
                var t_amt = 0;
                if(frm.doc.job_worker_table){
                    if(!frm.doc.job_worker_table.length){
                        if(frm.doc.items && frm.is_new()){
                            cur_frm.doc.items.forEach((item)=>{
                                if(item.sales_order){
                                    frappe.db.get_value("Sales Order",{'name':item.sales_order},"work").then((work)=>{
                                        if(work.message.work === "Supply and Laying")
                                        {
                                            frappe.db.get_value('Item', {'item_code':item.item_code}, 'laying_cost').then((data)=>{
                                                if(item.item_group != "Raw Material"){
                                                var new_row = cur_frm.add_child("job_worker_table");
                                                frappe.model.set_value(new_row.doctype,new_row.name,"item_code",item.item_code)
                                                frappe.model.set_value(new_row.doctype,new_row.name,"sqft",item.qty)
                                                frappe.model.set_value(new_row.doctype,new_row.name,"ratesqft",data.message.laying_cost)
                                                frappe.model.set_value(new_row.doctype,new_row.name,"ts_amount",item.qty * data.message.laying_cost)
                                                t_amt+=(item.qty * data.message.laying_cost)
                                                cur_frm.set_value("total_amount_job_worker",t_amt)
                                                }
                                            })
                                        }
                                    })
                                    
                                }
                            })       
                            
                        }
                    }
                }
        },
        validate:function(frm){
            if(frm.doc.job_worker_table){
               for(var i=0;i<frm.doc.job_worker_table.length;i++){
                  frm.doc.job_worker_table[i].ts_amount = frm.doc.job_worker_table[i].ratesqft * frm.doc.job_worker_table[i].sqft  
               }
        }
        
    }
        })


function amount(frm,cdt,cdn){
    let row=locals[cdt][cdn];
    if(row.qty>=0 && row.rate>=0){
        frappe.model.set_value(cdt,cdn,'amount',Math.round(row.qty*row.rate));
    }
 }
 frappe.ui.form.on('Sales Invoice Print Items', {
     qty:function(frm,cdt,cdn){
         amount(frm,cdt,cdn);
        },
     rate:function(frm,cdt,cdn){
         amount(frm,cdt,cdn);
        },
    })

frappe.ui.form.on('Sales Invoice',{
    refresh:function(frm){
        if(cur_frm.doc.docstatus==0){
            cur_frm.fields_dict.site_work.$input.on("click", function() {
                if(!cur_frm.doc.customer){
                    frappe.throw('Please Select Customer')
                }
            });
        }
    },
    customer:function(frm){
        cur_frm.set_value('site_work','')
        frm.set_query('site_work',function(frm){
            return {
                filters:{
                    'customer': cur_frm.doc.customer,
                    'status': 'Open',
                    'is_multi_customer':1
                }
            }
        })
    },
})
frappe.ui.form.on('TS Job Worker Salary',{
    ratesqft:function(frm,cdt,cdn){
        var ts_rate = locals[cdt][cdn]
        frappe.model.set_value(cdt,cdn,"ts_amount",ts_rate.ratesqft * ts_rate.sqft)
    },
    sqft:function(frm,cdt,cdn){
        var ts_rate = locals[cdt][cdn]
        frappe.model.set_value(cdt,cdn,"ts_amount",ts_rate.ratesqft * ts_rate.sqft)  
    },
    ts_amount:function(frm,cdt,cdn){
        total_calculation(frm)  
    },
    job_worker_table_remove:function(frm, cdt, cdn){
        total_calculation(frm)
    },
    item_code: function(frm,cdt,cdn){
        let row = locals[cdt][cdn]
        frappe.db.get_value('Item', row.item_code, 'loading_cost').then((data)=>{
            frappe.model.set_value(cdt, cdn, 'ratesqft', data.message.loading_cost)
        })
    }
   
})
function total_calculation(frm){
    var ts_amt = 0;
        frm.doc.job_worker_table.forEach((data)=>{
            ts_amt+= data.ts_amount
        
        })
        cur_frm.set_value("total_amount_job_worker",ts_amt)
}

