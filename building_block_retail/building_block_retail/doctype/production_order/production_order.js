// Copyright (c) 2023, Thirvusoft and contributors
// For license information, please see license.txt

frappe.ui.form.on('Production Order', {
	refresh: function(frm) {
        var button = cur_frm.fields_dict.works.grid.add_custom_button("Refresh", ()=>{
            frm.call({
                doc:frm.doc,
                method: 'refresh_works',
                callback(r){
                    frm.reload_doc()
                }
            })
        })
        button[0].style.backgroundColor = '#2490ef' 
        button[0].style.color = 'white' 
        frm.events.today_produced_item_filter(frm)
        frm.set_query("item_template", function () {
            return {
                filters: {
                    has_variants:1
                }
            }
        })
        let items =[];
        for(let i = 0; i<(frm.doc.production_order_details || []).length; i++){
                items.push(frm.doc.production_order_details[i].item_code)
        }
        frm.set_query("from_job_card", "excess_and_shortage", function () {
            return {
                filters: {
                    production_item:['in', items]
                }
            }
        })
        if(!frm.is_new()){
            frm.add_custom_button('Make Job Card', function(){
                if(!frm.doc.today_produced_items || !frm.doc.today_produced_items.length){
                    frappe.show_alert({message:"Enter Today Produced Items with Qty", indicator: 'red'})
                    frm.scroll_to_field('today_produced_items')
                }
                else{
                    var d = new frappe.ui.Dialog({
                        title:'Select Employee',
                        fields:[
                            {fieldname:'employee', label:'Employee', fieldtype:'Link', options:'Employee', reqd:1},
                            {fieldname:'workstation', label:'Workstation', fieldtype:'Link', options:'Workstation', reqd:1}
                        ],
                        primary_action(data){
                            frm.call({
                                doc:frm.doc,
                                method: 'make_job_card',
                                args: {
                                    'employee':data.employee,
                                    'workstation':data.workstation
                                },
                                callback(r){
                                    frm.reload_doc()
                                    d.hide()
                                    if(r.message){
                                        frappe.show_alert(`<p>Job Card(s) are Created.</p><p>${r.message}</p>`)
                                    }
                                }
                            })
                        }
                    })
                    d.show()
                }
            })

            frm.add_custom_button("Update Work Order", function(){
                frm.call({
                    doc:frm.doc,
                    method:"update_work_order",
                    callback(r){
                        frappe.show_alert("Work Orders Updated.")
                    }
                })
            })
        }
        frappe.realtime.off("no_qty_update_work_order")
        frappe.realtime.on("no_qty_update_work_order", ()=>{
            frappe.show_alert({
                message: "Please update today produced qty in Production Order Details",
                indicator: "red"
            })
            frm.scroll_to_field('production_order_details')
        })

        frappe.realtime.off("reload_doc")
        frappe.realtime.on("reload_doc", ()=>{
            frm.reload_doc()
        })
        
	},
    today_produced_item_filter: function(frm){
        let items =[];
        if(frm.doc.item_wise_production_qty){
            for(let i = 0; i<frm.doc.item_wise_production_qty.length; i++){
                if(frm.doc.item_wise_production_qty[i].qty){
                    items.push(frm.doc.item_wise_production_qty[i].item_code)
                }
            }
        }
       
        frm.set_query("item_code", "today_produced_items", function(){
            return {
                filters:{
                    'name':['in', items]
                }
            }
        })
        if(frm.doc.is_template){
            frm.set_query("item_code", "excess_and_shortage", function(){
                return {
                    filters:{
                        'variant_of':frm.doc.name
                    }
                }
            })
        }
        else{
            frm.set_query("item_code", "excess_and_shortage", function(){
                return {
                    filters:{
                        'name':frm.doc.name
                    }
                }
            })
        }
        
    },
    calculate_final_qty: function(frm, cdt, cdn){
        var row = locals[cdt][cdn]
        frappe.model.set_value(cdt, cdn, 'final_qty', row.produced_qty - row.excess_qty + row.shortage_qty)
    },
});

frappe.ui.form.on("Item Wise Production Qty", {
    item_code: function(frm){
        frm.events.today_produced_item_filter(frm)
    },
    item_wise_production_qty_add: function(frm){
        frm.events.today_produced_item_filter(frm)
    },
    item_wise_production_qty_remove: function(frm){
        frm.events.today_produced_item_filter(frm)
    }
})

frappe.ui.form.on("Production Order Item", {
    today_produced_qty: function(frm, cdt, cdn){
        var row = locals[cdt][cdn]
        if(row.today_produced_qty < 0){
            frappe.model.set_value(cdt, cdn, 'today_produced_qty', 0)
            frappe.throw("Today Produced Qty Cannot be Negative")
        }

        var item_wise_qty = {}
        for(let i=0; i<frm.doc.production_order_details.length; i++){
            if(Object.keys(item_wise_qty).includes(frm.doc.production_order_details[i].item_code)){
                item_wise_qty[frm.doc.production_order_details[i].item_code] += frm.doc.production_order_details[i].today_produced_qty
            }
            else{
                item_wise_qty[frm.doc.production_order_details[i].item_code] = frm.doc.production_order_details[i].today_produced_qty
            }
        }
        for(let i=0; i<frm.doc.item_wise_production_qty.length; i++){
            if(Object.keys(item_wise_qty).includes(frm.doc.item_wise_production_qty[i].item_code)){
                var row = locals[frm.doc.item_wise_production_qty[i].doctype][frm.doc.item_wise_production_qty[i].name]
                frappe.model.set_value(frm.doc.item_wise_production_qty[i].doctype, frm.doc.item_wise_production_qty[i].name, 'pending_qty_to_allocate_in_work_order', row.qty_to_update_in_work_order - item_wise_qty[frm.doc.item_wise_production_qty[i].item_code])
            }
        }
        frm.refresh_field("item_wise_production_qty")

    }
})


frappe.ui.form.on("Today Produced Items", {
    item_code: function(frm, cdt, cdn){
        let row = locals[cdt][cdn]
        let items = {}
        if(!frm.doc.excess_and_shortage){
            return
        }
        for(let i=0; i<frm.doc.excess_and_shortage.length; i++){
            if(Object.keys(items).includes(frm.doc.excess_and_shortage[i].item_code)){
                items[frm.doc.excess_and_shortage[i].item_code]['excess_qty'] += (frm.doc.excess_and_shortage[i].excess_qty || 0)
                items[frm.doc.excess_and_shortage[i].item_code]['shortage_qty'] += (frm.doc.excess_and_shortage[i].shortage_qty || 0)
            }
            else{
                items[frm.doc.excess_and_shortage[i].item_code] = {
                    "excess_qty":(frm.doc.excess_and_shortage[i].excess_qty || 0),
                    "shortage_qty":(frm.doc.excess_and_shortage[i].shortage_qty || 0)
                }
            }
        }
        if(Object.keys(items).includes(row.item_code)){
            frappe.model.set_value(cdt, cdn, "excess_qty", items[row.item_code]["excess_qty"])
            frappe.model.set_value(cdt, cdn, "shortage_qty", items[row.item_code]["shortage_qty"])
        }
    }
})


frappe.ui.form.on("Production Order Excess and Shortage", {
    item_code: function(frm, cdt, cdn){
        var row = locals[cdt][cdn]
        frm.set_query("from_job_card", "excess_and_shortage", function () {
            return {
                filters: {
                    production_item:row.item_code
                }
            }
        })
    }
})


// Code Reference : https://www.w3schools.com/howto/tryit.asp?filename=tryhow_js_draggable
function dragElement(dialog) {
  var elmnt = dialog.$wrapper.find('#mydiv')[0]
  var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
  if (dialog.$wrapper.find('#mydivheader').length) {
    /* if present, the header is where you move the DIV from:*/
    dialog.$wrapper.find('#mydivheader')[0].onmousedown = dragMouseDown;
  } else {
    /* otherwise, move the DIV from anywhere inside the DIV:*/
    elmnt.onmousedown = dragMouseDown;
  }

  function dragMouseDown(e) {
    e = e || window.event;
    e.preventDefault();
    // get the mouse cursor position at startup:
    pos3 = e.clientX;
    pos4 = e.clientY;
    document.onmouseup = closeDragElement;
    // call a function whenever the cursor moves:
    document.onmousemove = elementDrag;
  }

  function elementDrag(e) {
    e = e || window.event;
    e.preventDefault();
    // calculate the new cursor position:
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;
    // set the element's new position:
    elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
    elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
  }

  function closeDragElement() {
    /* stop moving when mouse button is released:*/
    document.onmouseup = null;
    document.onmousemove = null;
  }
}