// Copyright (c) 2024, Ramesh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Custom Work Order", {
    refresh(frm) {
        frm.add_custom_button(
            ("Get Items From Sales Order"),
            function () {
                // Create a dialog box
                let dialog = new frappe.ui.Dialog({
                    title: "Select Sales Orders",
                    fields: [
                        {
                            label: "Sales Orders",
                            fieldname: "sales_orders",
                            fieldtype: "Table MultiSelect",
                            options: "Sales Order Items",
                            reqd: 1,
                        }
                    ],
                    primary_action_label: "Get Items",
                    primary_action(values) {
                        // Get selected sales orders
                        let selected_sales_orders = values.sales_orders || [];

                        if (selected_sales_orders.length > 0) {
                            let sales_order_ids = selected_sales_orders.map(so => so.sales_order);
                            // Call server-side function to fetch items
                            frappe.call({
                                method: "ramesh_interview_solution.ramesh_interview_solution.doctype.custom_work_order.custom_work_order.get_sales_order_items",
                                args: {
                                    sales_orders: sales_order_ids
                                },
                                callback: function (r) {
                                    if (r.message) {
                                        let items = r.message;
                                        // Insert fetched items into the child table
                                        items.forEach(function (item) {
                                            let child = frm.add_child("work_order_items");
                                            child.sales_order = item.sales_order;
                                            child.item = item.item_code;
                                            child.qty = item.qty;
                                        });
                                        frm.refresh_field("work_order_items");
                                    }
                                }
                            });
                        } else {
                            frappe.msgprint("Please select at least one sales order.");
                        }

                        dialog.hide();
                    }
                });

                // Show the dialog box
                dialog.show();
            },
        );
    },
});
