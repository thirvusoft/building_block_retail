frappe.ui.form.on("Purchase Order", {
    onload: function(frm){
        setTimeout(() => {
			frm.remove_custom_button('Product Bundle', "Get Items From");
		}, 500);  
    }
})