// Copyright (c) 2024, Ramesh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Time Sheet", {
	refresh(frm) {
        if (frm.is_new()){
            frm.set_value("user_id", frappe.session.user)
            frm.refresh_field("user_id")
        }
	},
});
