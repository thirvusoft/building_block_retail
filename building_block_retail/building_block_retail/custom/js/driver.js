frappe.ui.form.on('Driver', {
    refresh: function(frm){
        frm.set_query('employee', function(frm){
            return{
                filters:{
                    'status':'Active'
                }
            }
        })
    }
})