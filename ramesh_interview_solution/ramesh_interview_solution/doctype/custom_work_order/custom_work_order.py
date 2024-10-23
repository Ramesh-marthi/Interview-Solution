# Copyright (c) 2024, Ramesh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json
from frappe.utils import random_string, nowdate

class CustomWorkOrder(Document):
	pass



@frappe.whitelist()
def get_sales_order_items(sales_orders):
    sales_orders = json.loads(sales_orders)
    # sales_orders =  [ "SAL-ORD-2024-00001","SAL-ORD-2024-00002"] 
    items = []
    for sales_order in sales_orders:
        sales_order_doc = frappe.get_doc("Sales Order", sales_order)
        for item in sales_order_doc.items:
            items.append({
                "sales_order": sales_order,  
                "item_code": item.item_code,  
                "qty": item.qty 
            })
    return items


@frappe.whitelist()
def create_custom_work_order(data):
    items_list = json.loads(data)
    
    custom_work_order = frappe.get_doc({
        'doctype': 'Custom Work Order',
        'work_order_name': random_string(5) + '-' + nowdate(),  
    })
    
    for item in items_list:
        custom_work_order.append('work_order_items', {
            'sales_order': item['parent'],
            'item': item['item_code'],
            'qty': item['qty'],
           
        })
    
    custom_work_order.insert()
    frappe.db.commit()

    return custom_work_order.name
