frappe.ui.form.on("Purchase Order", {
    onload: function(frm){
        setTimeout(() => {
			frm.remove_custom_button('Product Bundle', "Get Items From");
		}, 500);  
    },
    schedule_date: function(frm){
        frm.doc.items.forEach( (row)=>{
            row.schedule_date = frm.doc.schedule_date
        })
        frm.refresh()
    }
})