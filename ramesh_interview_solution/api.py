import frappe
import json

@frappe.whitelist()
def customer_api():
    try:
        data = frappe.form_dict
        
        if frappe.request.method == "POST":
            if frappe.get_value("Customer", {"customer_name": data.get("customer_name")}):
                return {"status": 409, "message": "Customer already exists"}

            doc = prepare_customer_doc(data, is_new=True)

            saved_customer = save(json.dumps(doc))
            return {"status": 201, "message": "Customer created successfully", "customer": saved_customer["name"]}

        elif frappe.request.method == "PUT":
            customer_name = frappe.get_value("Customer", {"customer_name": data.get("customer_name")})
            if not customer_name:
                return {"status": 404, "message": "Customer not found"}
            
            customer_doc = frappe.get_doc("Customer", customer_name)
            
            update_primary_address(customer_doc, data)
            update_primary_contact(customer_doc, data)
            return {"status": 200, "message": "Customer updated successfully", "customer": customer_doc.name}

        else:
            return {"status": 405, "message": "Method Not Allowed"}

    except KeyError as e:
        frappe.log_error(f"Missing field: {str(e)}", "Customer API Error - KeyError")
        return {"status": 400, "error": f"Missing required field: {str(e)}"}
    
    except Exception as e:
        frappe.log_error(f"Error in customer_api: {frappe.get_traceback()}", "Customer API Error - General Exception")
        return {"status": 500, "error": "Internal Server Error"}

def prepare_customer_doc(data, is_new):
    """
    Prepare the customer doc structure for the save function.
    If is_new is True, create a new customer, else update an existing one.
    """
    doc = {
        "docstatus": 0,
        "doctype": "Customer",
        "customer_name": data.get("customer_name"),
        "address_line1": data.get("address_line1"),
        "address_line2": data.get("address_line2"),
        "city": data.get("city"),
        "country": data.get("country"),
        "email_id": data.get("email_address"),
        "mobile_no": data.get("mobile_number"),
        "owner": frappe.session.user,
    }

    if is_new:
        doc["naming_series"] = "CUST-.YYYY.-"
        doc["customer_type"] = "Company"  # Set to company by default; adjust as needed
        doc["__islocal"] = 1  # Mark as a new document
        doc["__unsaved"] = 1
    return doc

def update_customer_fields(doc, data):
    """
    Update the fields of the customer document with new data from the request.
    """
    doc.customer_name = data.get("customer_name", doc.customer_name)
    doc.address_line1 = data.get("address_line1", doc.address_line1)
    doc.address_line2 = data.get("address_line2", doc.address_line2)
    doc.city = data.get("city", doc.city)
    doc.country = data.get("country", doc.country)
    doc.email_id = data.get("email_address", doc.email_id)
    doc.mobile_no = data.get("mobile_number", doc.mobile_no)

    
def update_primary_address(customer_doc, data):
    """
    Update the primary address for the customer.
    """
    # Fetch the primary address linked to the customer
    primary_address = frappe.get_value("Address", {"customer": customer_doc.name, "is_primary_address": 1})

    if primary_address:
        address_doc = frappe.get_doc("Address", primary_address)
        address_doc.address_line1 = data.get("address_line1", address_doc.address_line1)
        address_doc.address_line2 = data.get("address_line2", address_doc.address_line2)
        address_doc.city = data.get("city", address_doc.city)
        address_doc.pincode = data.get("pincode", address_doc.pincode)  # Make sure to include this field
        address_doc.state = data.get("state", address_doc.state)
        address_doc.country = data.get("country", address_doc.country)
        address_doc.save(ignore_permissions=True)

def update_primary_contact(customer_doc, data):
    """
    Update the primary contact for the customer.
    """
    # Fetch the primary contact linked to the customer
    primary_contact = frappe.get_value("Contact", {"customer": customer_doc.name, "is_primary_contact": 1})

    if primary_contact:
        contact_doc = frappe.get_doc("Contact", primary_contact)
        contact_doc.mobile_no = data.get("mobile_number", contact_doc.mobile_no)
        contact_doc.email_id = data.get("email_address", contact_doc.email_id)
        contact_doc.save(ignore_permissions=True)

@frappe.whitelist(methods=["POST"])
def save(doc):
    """
    Save the document.
    """
    if isinstance(doc, str):
        doc = json.loads(doc)

    # Create a Frappe doc and save
    doc = frappe.get_doc(doc)
    doc.flags.ignore_permissions = True  
    doc.save()

    return doc.as_dict()
