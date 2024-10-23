frappe.ui.form.on("Sales Order", {
    refresh(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(
                __("Create Workflow"), 
                function () {
                    
                    frappe.call({
                        method: "ramesh_interview_solution.ramesh_interview_solution.doctype.custom_work_order.custom_work_order.create_custom_work_order",
                        args: {
                            'data': JSON.stringify(frm.doc.items), 
                        },
                        callback: function(r) {
                            
                            if (!r.exc && r.message) {
                                const work_order_link = frappe.utils.get_form_link('Custom Work Order', r.message);

                                frappe.msgprint({
                                    title: __('Success'),
                                    message: __(`Custom Work Order created successfully! <br><a href="${work_order_link}" target="_blank">View Work Order</a>`),
                                    indicator: 'green'
                                });
                                
                            } else {
                                frappe.msgprint({
                                    title: __('Error'),
                                    message: __('There was an issue creating the Work Order.'),
                                    indicator: 'red'
                                });
                            }
                        },
                        
                    });
                }
            );
        }
    },
});
