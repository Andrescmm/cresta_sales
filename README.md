# cresta_sales

# Installing an Odoo Module

Follow these steps to install and configure a custom module in your Odoo instance.

---

## 1. Prepare Your Environment
Before installing the module, ensure you have the following prerequisites:
- A running Odoo instance.
- Access to the Odoo server or a development environment.
- Basic understanding of Odoo's file structure.

---

## 2. Copy the Module
1. Locate the module folder, typically named something like `project_management`, `custom_module`, etc.
2. Copy the module folder to the Odoo `addons` directory. This directory is usually located at:
   - **Linux**: `/opt/odoo/addons` (default installation)
   - **Windows**: `C:\Program Files (x86)\Odoo 15\server\addons`
   - **Custom Path**: As defined in your `odoo.conf` file under the `addons_path`.

---

## 3. Update Module List
1. Restart the Odoo server to ensure it recognizes the new module.
   - **Command**:
     ```bash
     sudo service odoo restart
     ```
     Or, if running Odoo manually:
     ```bash
     ./odoo-bin -c /etc/odoo/odoo.conf
     ```
2. Log in to your Odoo instance as an admin.
3. Go to **Apps** (from the main menu).
4. Click the **Update Apps List** option from the **Apps** menu (top-right corner).

---

## 4. Install the Module
1. Search for the module by its name (e.g., "Project Management") in the Apps menu.
2. If the module is not visible:
   - Ensure the **"Apps" filter** is cleared or set to **"All"**.
   - Verify the module folder is in the correct `addons` path.
   - Check for syntax errors in the module by reviewing server logs.
3. Once found, click the **Install** button.

---

## 5. Troubleshooting Installation Errors
- **Missing Dependencies**:  
   Install any dependent modules listed in the error message.
- **Python Libraries**:  
   If a required library is missing, install it using pip:
   ```bash
   pip install <library_name>
