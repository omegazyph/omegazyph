# Date: 2026-01-25
# Script Name: vault_hacker_gui.pyw
# Author: omegazyph
# Updated: 2026-01-25
# Description: Stealth AES-256 Vault with Instant Dialog Focus and Browser Integration.
# Features: Full non-shorthand logic, Windowless execution, and Forced Dialog Foreground.

import os
import json
import base64
import secrets
import string
import shutil
import webbrowser
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime

# Cryptography imports
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

class HackerVaultGUI:
    def __init__(self, root):
        """
        Initializes the wide-view stealth GUI and ensures input dialogs appear in the foreground.
        """
        self.root = root
        self.root.title("SYSTEM_ACCESS: CIPHER_VAULT_PRO")
        
        # Withdraw the root window while the authentication dialog is active
        self.root.withdraw()
        
        self.root.geometry("1150x650")
        self.bg_color = "#000000"
        self.fg_color = "#00FF41" 
        self.font_style = ("Courier New", 10, "bold")
        self.root.configure(bg=self.bg_color)

        # File path configuration
        script_path_absolute = os.path.abspath(__file__)
        script_directory = os.path.dirname(script_path_absolute)
        parent_directory = os.path.dirname(script_directory)
        
        self.data_directory = os.path.join(parent_directory, "data")
        self.backup_directory = os.path.join(self.data_directory, "backups")
        self.file_path = os.path.join(self.data_directory, "vault_data.bin")

        # Create necessary directories if they do not exist
        if not os.path.exists(self.data_directory):
            os.makedirs(self.data_directory)
        if not os.path.exists(self.backup_directory):
            os.makedirs(self.backup_directory)

        # Force the authentication dialog to the front
        self.master_password = simpledialog.askstring("SECURE_AUTH", "ENTER MASTER KEY:", show='*', parent=self.root)
        
        if self.master_password is None or self.master_password == "":
            self.root.destroy()
            return

        self.key = self.derive_cryptographic_key(self.master_password)
        self.cipher = Fernet(self.key)
        
        # Show the main window after successful key derivation
        self.root.deiconify()
        self.setup_hacker_user_interface()

    def derive_cryptographic_key(self, password):
        """
        Derives a cryptographic key using PBKDF2 with a static salt.
        """
        salt = b'static_salt_for_omegazyph'
        key_derivation_function = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        password_encoded = password.encode()
        derived_key = key_derivation_function.derive(password_encoded)
        return base64.urlsafe_b64encode(derived_key)

    def setup_hacker_user_interface(self):
        """
        Configures the graphical user interface elements.
        """
        header_label = tk.Label(
            self.root, 
            text=">_ CIPHER_VAULT: PRO_EDITION_ACTIVE", 
            font=("Courier New", 16, "bold"), 
            bg=self.bg_color, 
            fg=self.fg_color
        )
        header_label.pack(pady=15)

        # Configure styling for the data grid (Treeview)
        interface_style = ttk.Style()
        interface_style.theme_use("clam")
        interface_style.configure(
            "Treeview", 
            background=self.bg_color, 
            foreground=self.fg_color, 
            fieldbackground=self.bg_color, 
            font=self.font_style, 
            rowheight=30
        )
        interface_style.map("Treeview", background=[('selected', '#003300')])
        interface_style.configure(
            "Treeview.Heading", 
            background="#111111", 
            foreground=self.fg_color, 
            font=self.font_style
        )

        treeview_frame = tk.Frame(self.root, bg=self.bg_color)
        treeview_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=25)

        column_identifiers = ("Service", "Website", "Username", "Last Updated")
        self.data_grid = ttk.Treeview(treeview_frame, columns=column_identifiers, show='headings')
        
        for column in column_identifiers:
            self.data_grid.heading(column, text=f"[ {column.upper()} ]")
        
        self.data_grid.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Bind double-click event to open website
        self.data_grid.bind("<Double-1>", lambda event: self.open_associated_website())

        button_container = tk.Frame(self.root, bg=self.bg_color)
        button_container.pack(pady=20)
        
        button_config = {
            "bg": "#111111", 
            "fg": self.fg_color, 
            "activebackground": self.fg_color, 
            "activeforeground": self.bg_color, 
            "font": self.font_style, 
            "width": 12, 
            "relief": "flat"
        }

        tk.Button(button_container, text="ADD_NEW", command=self.add_vault_entry, **button_config).grid(row=0, column=0, padx=5)
        tk.Button(button_container, text="EDIT_ENTRY", command=self.edit_vault_entry, **button_config).grid(row=0, column=1, padx=5)
        tk.Button(button_container, text="VIEW_DETAILS", command=self.view_vault_entry, **button_config).grid(row=0, column=2, padx=5)
        tk.Button(button_container, text="OPEN_LINK", command=self.open_associated_website, **button_config).grid(row=0, column=3, padx=5)
        tk.Button(button_container, text="COPY_PASS", command=self.copy_password_to_clipboard, **button_config).grid(row=0, column=4, padx=5)
        tk.Button(button_container, text="DELETE", command=self.delete_vault_entry, **button_config).grid(row=0, column=5, padx=5)
        tk.Button(button_container, text="TERMINATE", command=self.root.destroy, **button_config).grid(row=0, column=6, padx=5)

        self.status_message_variable = tk.StringVar(value="SYSTEM_READY")
        status_bar_label = tk.Label(
            self.root, 
            textvariable=self.status_message_variable, 
            bd=1, 
            relief="sunken", 
            anchor="w",
            bg="#111111", 
            fg=self.fg_color, 
            font=("Courier New", 9)
        )
        status_bar_label.pack(side=tk.BOTTOM, fill=tk.X)

        self.refresh_data_grid()

    def open_associated_website(self):
        """
        Retrieves the URL from the selected row and opens it in the default browser.
        """
        current_selection = self.data_grid.selection()
        if not current_selection:
            return
            
        selected_item_data = self.data_grid.item(current_selection)
        website_url = selected_item_data['values'][1]
        
        if website_url and website_url != "N/A":
            if not website_url.lower().startswith("http"):
                website_url = "https://" + website_url
            
            self.status_message_variable.set(f"LAUNCHING_BROWSER: {website_url}")
            webbrowser.open(website_url)
        else:
            messagebox.showwarning("INVALID_LINK", "NO VALID URL DETECTED FOR THIS ENTRY.")

    def auto_resize_grid_columns(self):
        """
        Adjusts column widths based on the content.
        """
        import tkinter.font as tkfont
        grid_font = tkfont.Font(font=self.font_style)
        for column in self.data_grid["columns"]:
            header_label_text = f"[ {column.upper()} ]"
            maximum_width = grid_font.measure(header_label_text) + 50
            for row_id in self.data_grid.get_children():
                cell_content = str(self.data_grid.set(row_id, column))
                content_width = grid_font.measure(cell_content) + 50
                if content_width > maximum_width:
                    maximum_width = content_width
            self.data_grid.column(column, width=maximum_width)

    def load_encrypted_vault(self):
        """
        Reads and decrypts the vault data file.
        """
        if not os.path.exists(self.file_path):
            return {}
        try:
            with open(self.file_path, "rb") as vault_file:
                encrypted_bytes = vault_file.read()
                decrypted_bytes = self.cipher.decrypt(encrypted_bytes)
                decrypted_string = decrypted_bytes.decode()
                return json.loads(decrypted_string)
        except Exception:
            messagebox.showerror("ACCESS_DENIED", "AUTHENTICATION_FAILED: INVALID MASTER KEY")
            self.root.destroy()
            return None

    def refresh_data_grid(self):
        """
        Reloads the information from the vault into the display grid.
        """
        for item in self.data_grid.get_children():
            self.data_grid.delete(item)
        vault_information = self.load_encrypted_vault()
        if vault_information is not None:
            for service_identifier in sorted(vault_information.keys()):
                entry_data = vault_information[service_identifier]
                self.data_grid.insert("", tk.END, values=(
                    service_identifier, 
                    entry_data.get("website", "N/A"), 
                    entry_data.get("username", "N/A"),
                    entry_data.get("last_updated", "UNKNOWN")
                ))
            self.auto_resize_grid_columns()

    def add_vault_entry(self):
        """
        Prompts user for new entry details and ensures dialog focus.
        """
        # Momentarily force main window to be non-topmost to allow dialog to appear on top
        self.root.attributes("-topmost", False)
        
        service_name = simpledialog.askstring("SYSTEM_INPUT", "TARGET_SERVICE:", parent=self.root)
        if not service_name:
            return
        website_address = simpledialog.askstring("SYSTEM_INPUT", "TARGET_URL:", parent=self.root)
        user_identity = simpledialog.askstring("SYSTEM_INPUT", "IDENT_USER:", parent=self.root)
        secret_password = simpledialog.askstring("SYSTEM_INPUT", "SECRET_KEY (LEAVE BLANK FOR AUTO-GEN):", parent=self.root)
        
        if not secret_password:
            character_pool = string.ascii_letters + string.digits + "!@#$%^&*"
            secret_password = "".join(secrets.choice(character_pool) for index in range(20))
            messagebox.showinfo("GEN_SUCCESS", f"GENERATED_PASSWORD: {secret_password}")
            
        vault_information = self.load_encrypted_vault()
        if vault_information is not None:
            vault_information[service_name] = {
                "website": website_address if website_address else "N/A", 
                "username": user_identity, 
                "password": secret_password, 
                "last_updated": datetime.now().strftime("%Y-%m-%d")
            }
            self.save_encrypted_vault(vault_information)
            self.refresh_data_grid()

    def edit_vault_entry(self):
        """
        Allows the user to modify an existing entry's fields with forced dialog focus.
        """
        current_selection = self.data_grid.selection()
        if not current_selection:
            return
            
        selected_item_data = self.data_grid.item(current_selection)
        service_name = selected_item_data['values'][0]
        
        vault_information = self.load_encrypted_vault()
        if vault_information and service_name in vault_information:
            entry_info = vault_information[service_name]
            
            # Request updated information with explicit parent focus
            new_website = simpledialog.askstring("EDIT_FIELD", f"UPDATE URL FOR {service_name}:", initialvalue=entry_info.get("website"), parent=self.root)
            new_username = simpledialog.askstring("EDIT_FIELD", f"UPDATE USER FOR {service_name}:", initialvalue=entry_info.get("username"), parent=self.root)
            new_password = simpledialog.askstring("EDIT_FIELD", f"UPDATE PASSWORD FOR {service_name}:", initialvalue=entry_info.get("password"), parent=self.root)
            
            if new_website is not None and new_username is not None and new_password is not None:
                vault_information[service_name] = {
                    "website": new_website,
                    "username": new_username,
                    "password": new_password,
                    "last_updated": datetime.now().strftime("%Y-%m-%d")
                }
                self.save_encrypted_vault(vault_information)
                self.refresh_data_grid()
                self.status_message_variable.set(f"RECORD_UPDATED: {service_name}")

    def view_vault_entry(self):
        """
        Shows decrypted details for a selected entry.
        """
        current_selection = self.data_grid.selection()
        if not current_selection:
            return
        selected_item_data = self.data_grid.item(current_selection)
        service_identifier = selected_item_data['values'][0]
        vault_information = self.load_encrypted_vault()
        if vault_information and service_identifier in vault_information:
            entry_info = vault_information[service_identifier]
            display_text = (
                f"SERVICE:  {service_identifier}\n"
                f"URL:      {entry_info.get('website')}\n"
                f"IDENTITY: {entry_info.get('username')}\n"
                f"PASSWORD: {entry_info.get('password')}"
            )
            messagebox.showinfo("DECRYPTED_RECORD", display_text)

    def copy_password_to_clipboard(self):
        """
        Copies the password and clears it after 30 seconds.
        """
        current_selection = self.data_grid.selection()
        if not current_selection:
            return
        service_identifier = self.data_grid.item(current_selection)['values'][0]
        vault_information = self.load_encrypted_vault()
        if vault_information and service_identifier in vault_information:
            self.root.clipboard_clear()
            self.root.clipboard_append(vault_information[service_identifier]['password'])
            self.status_message_variable.set("CLIPBOARD_STATUS: PASSWORD_COPIED (30S TIMER)")
            self.root.after(30000, lambda: self.root.clipboard_clear())

    def delete_vault_entry(self):
        """
        Removes a service from the vault database.
        """
        current_selection = self.data_grid.selection()
        if not current_selection:
            return
        service_identifier = self.data_grid.item(current_selection)['values'][0]
        user_confirmation = messagebox.askyesno("CONFIRM", f"PERMANENTLY DELETE {service_identifier}?", parent=self.root)
        if user_confirmation:
            vault_information = self.load_encrypted_vault()
            if vault_information and service_identifier in vault_information:
                del vault_information[service_identifier]
                self.save_encrypted_vault(vault_information)
                self.refresh_data_grid()

    def save_encrypted_vault(self, vault_data):
        """
        Encrypts and saves the vault data and creates a backup.
        """
        data_json_string = json.dumps(vault_data)
        data_encoded_bytes = data_json_string.encode()
        encrypted_data_bytes = self.cipher.encrypt(data_encoded_bytes)
        
        with open(self.file_path, "wb") as vault_file_handle:
            vault_file_handle.write(encrypted_data_bytes)
            
        timestamp_formatted = datetime.now().strftime("%Y%m%d_%H%M%S")
        if not os.path.exists(self.backup_directory):
            os.makedirs(self.backup_directory)
        
        backup_file_path = os.path.join(self.backup_directory, f"backup_{timestamp_formatted}.bin")
        shutil.copy2(self.file_path, backup_file_path)

if __name__ == "__main__":
    root_window = tk.Tk()
    application_instance = HackerVaultGUI(root_window)
    root_window.mainloop()