import requests
import frappe

NEXTCLOUD_URL = frappe.conf.get("nextcloud_url")
NEXTCLOUD_USER = frappe.conf.get("nextcloud_user")
NEXTCLOUD_PASSWORD = frappe.conf.get("nextcloud_password")

def upload_to_nextcloud(file_doc):
    """Uploads ERPNext file to Nextcloud via WebDAV and saves the file URL in ERPNext."""
    file_path = file_doc.get_full_path()
    file_name = file_doc.file_name

    with open(file_path, 'rb') as f:
        response = requests.put(
            f"{NEXTCLOUD_URL}{file_name}",
            auth=(NEXTCLOUD_USER, NEXTCLOUD_PASSWORD),
            data=f
        )

    if response.status_code == 201:
        nextcloud_link = f"{NEXTCLOUD_URL}{file_name}"
        frappe.msgprint(f"File uploaded to Nextcloud: {nextcloud_link}")
        
        # Save Nextcloud URL in ERPNext file record
        file_doc.db_set("file_url", nextcloud_link)
    else:
        frappe.throw(f"Failed to upload file to Nextcloud: {response.status_code}, {response.text}")

def upload_after_insert(doc, method):
    """Trigger function when a file is uploaded to ERPNext."""
    upload_to_nextcloud(doc)
