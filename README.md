
### Problem Statement 1: Timesheet Management

- Created roles and permissions for **Timesheet User** and **Timesheet Manager**.
- Implemented a workflow with states: Draft, Pending Approval, Need Modification, and Approved for Timesheets.
- Users can create Timesheets in Draft format; Managers can approve or send for modifications.
- Notifications are set up:
  - Managers notified upon Timesheet creation.
  - Users notified if modifications or approvals are required.

### Problem Statement 2: Custom Work Order from Sales Order

- Developed a new doctype **Custom Workorder** for manufacturing company needs.
- Linked to Sales Order for creating custom documents directly or for multiple orders.
- Added functionality:
  - **Get Items from Sales Order** button retrieves items from selected Sales Orders.
  - Integrated a button in Sales Order to generate **Custom Workorder** records.

**Detailed Changes:**
- Implemented role permissions and workflow states in ERPNext.
- Designed and developed the **Custom Workorder** doctype with necessary child table fields.
- Integrated buttons and dialog boxes for seamless interaction with Sales Orders.
- Ensured all operations adhere to ERPNext best practices and client requirements.
