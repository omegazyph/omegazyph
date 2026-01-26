# Date: 2026-01-25
# Script Name: vault_hacker_gui.pyw
# Author: omegazyph
# Updated: 2026-01-25
# Description: Stable AES-256 Vault with bound dialogs for forced foreground focus.
# Features: Full non-shorthand logic, parent-linked dialogs, and automatic HTTPS correction.

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
        Initializes the GUI and ensures it handles focus correctly on Windows 11.
        """
        self.root = root
        self.root.title("SYSTEM_ACCESS: CIPHER_VAULT_PRO")
        
        # Configure the main window appearance
        self.root.geometry("1150x650")
        self.bg_color = "#000000"
        self.fg_color = "#00FF41" 
        self.font_style = ("Courier New", 10, "bold")
        self.root.configure(bg=self.bg_color)

        # File and Directory Setup
        script_path_absolute = os.path.abspath(__file__)
        script_directory = os.path.dirname(script_path_absolute)
        parent_directory = os.path.dirname(script_directory)
        
        self.data_directory = os.path.join(parent_directory, "data")
        self.backup_directory = os.path.join(self.data_directory, "backups")
        self.file_path = os.path.join(self.data_directory, "vault_data.bin")

        # Create necessary folders if they are missing
        if not os.path.exists(self.data_directory):
            os.makedirs(self.data_directory)
        if not os.path.exists(self.backup_directory):
            os.makedirs(self.backup_directory)

        # Authenticate with master password
        # Using parent=self.root ensures the box doesn't hide behind other windows
        self.master_password = simpledialog.askstring(
            "SECURE_AUTH", 
            "ENTER MASTER KEY:", 
            show='*', 
            parent=self.root
        )
        
        if not self.master_password:
            self.root.destroy()
            return

        self.cryptographic_key = self.derive_cryptographic_key(self.master_password)
        self.cipher_engine = Fernet(self.cryptographic_key)
        
        # Verify the key by attempting to load the vault
        if os.path.exists(self.file_path):
            test_data = self.load_encrypted_vault()
            if test_data is None:
                messagebox.showerror("ACCESS_DENIED", "INVALID MASTER KEY", parent=self.root)
                self.root.destroy()
                return

        self.setup_hacker_user_interface()

    def derive_cryptographic_key(self, password):
        """
        Derives a secure 32-byte key from the provided password.
        """
        salt = b'static_salt_for_omegazyph'
        key_derivation_function = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        password_encoded = password.encode()
        derived_bytes = key_derivation_function.derive(password_encoded)
        return base64.urlsafe_b64encode(derived_bytes)

    def setup_hacker_user_interface(self):
        """
        Builds the visual elements of the application.
        """
        header_label = tk.Label(
            self.root, 
            text=">_ CIPHER_VAULT: FOREGROUND_STABLE", 
            font=("Courier New", 16, "bold"), 
            bg=self.bg_color, 
            fg=self.fg_color
        )
        header_label.pack(pady=15)

        # Treeview Configuration
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview", 
            background=self.bg_color, 
            foreground=self.fg_color, 
            fieldbackground=self.bg_color, 
            font=self.font_style, 
            rowheight=30
        )
        style.map("Treeview", background=[('selected', '#003300')])
        style.configure(
            "Treeview.Heading", 
            background="#111111", 
            foreground=self.fg_color, 
            font=self.font_style
        )

        self.data_grid = ttk.Treeview(
            self.root, 
            columns=("Service", "Website", "Username", "Last Updated"), 
            show='headings'
        )
        for col in ("Service", "Website", "Username", "Last Updated"):
            self.data_grid.heading(col, text=f"[ {col.upper()} ]")
        self.data_grid.pack(pady=10, fill=tk.BOTH, expand=True, padx=25)

        # Button Layout
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(pady=20)
        
        btn_config = {
            "bg": "#111111", 
            "fg": self.fg_color, 
            "font": self.font_style, 
            "width": 12, 
            "relief": "flat"
        }

        tk.Button(button_frame, text="ADD_NEW", command=self.add_vault_entry, **btn_config).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="EDIT_ENTRY", command=self.edit_vault_entry, **btn_config).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="OPEN_LINK", command=self.open_associated_website, **btn_config).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="COPY_PASS", command=self.copy_password_to_clipboard, **btn_config).grid(row=0, column=3, padx=5)
        tk.Button(button_frame, text="DELETE", command=self.delete_vault_entry, **btn_config).grid(row=0, column=4, padx=5)
        tk.Button(button_frame, text="EXIT", command=self.root.destroy, **btn_config).grid(row=0, column=5, padx=5)

        self.refresh_data_grid()

    def load_encrypted_vault(self):
        """
        Reads and decrypts the data file.
        """
        if not os.path.exists(self.file_path):
            return {}
        try:
            with open(self.file_path, "rb") as file_handle:
                encrypted_content = file_handle.read()
                decrypted_content = self.cipher_engine.decrypt(encrypted_content)
                return json.loads(decrypted_content.decode())
        except Exception:
            return None

    def save_encrypted_vault(self, vault_data):
        """
        Encrypts data and creates a dated backup.
        """
        json_data = json.dumps(vault_data).encode()
        encrypted_data = self.cipher_engine.encrypt(json_data)
        with open(self.file_path, "wb") as file_handle:
            file_handle.write(encrypted_data)
            
        # Automated Backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}.bin"
        shutil.copy2(self.file_path, os.path.join(self.backup_directory, backup_name))

    def refresh_data_grid(self):
        """
        Clears and re-populates the display grid.
        """
        for item in self.data_grid.get_children():
            self.data_grid.delete(item)
        vault_info = self.load_encrypted_vault()
        if vault_info:
            for service in sorted(vault_info.keys()):
                entry = vault_info[service]
                self.data_grid.insert("", tk.END, values=(
                    service, 
                    entry.get("website", "N/A"), 
                    entry.get("username", "N/A"), 
                    entry.get("last_updated", "UNKNOWN")
                ))

    def open_associated_website(self):
        """
        Opens the URL in the browser with case-insensitive protocol correction.
        """
        selection = self.data_grid.selection()
        if not selection:
            return
        url = self.data_grid.item(selection)['values'][1]
        if url and url != "N/A":
            # Corrects the HTTPS typo/case issue automatically
            if not url.lower().startswith("http"):
                url = "https://" + url
            webbrowser.open(url)

    def add_vault_entry(self):
        """
        Prompts for new data using parent-locked dialogs for visibility.
        """
        service = simpledialog.askstring("INPUT", "SERVICE NAME:", parent=self.root)
        if not service:
            return
        url = simpledialog.askstring("INPUT", "URL:", parent=self.root)
        user = simpledialog.askstring("INPUT", "USERNAME:", parent=self.root)
        pw = simpledialog.askstring("INPUT", "PASSWORD (BLANK FOR AUTO):", parent=self.root)
        
        if not pw:
            pw = "".join(secrets.choice(string.ascii_letters + string.digits) for i in range(20))
            
        vault = self.load_encrypted_vault()
        vault[service] = {
            "website": url or "N/A", 
            "username": user or "N/A", 
            "password": pw, 
            "last_updated": datetime.now().strftime("%Y-%m-%d")
        }
        self.save_encrypted_vault(vault)
        self.refresh_data_grid()

    def edit_vault_entry(self):
        """
        Allows modification of existing entries via parent-locked dialogs.
        """
        selection = self.data_grid.selection()
        if not selection:
            return
        service = self.data_grid.item(selection)['values'][0]
        vault = self.load_encrypted_vault()
        entry = vault[service]
        
        # Parent=self.root forces these to appear in front of the main window
        new_url = simpledialog.askstring("EDIT", "URL:", initialvalue=entry.get("website"), parent=self.root)
        new_user = simpledialog.askstring("EDIT", "USERNAME:", initialvalue=entry.get("username"), parent=self.root)
        new_pw = simpledialog.askstring("EDIT", "PASSWORD:", initialvalue=entry.get("password"), parent=self.root)
        
        if new_url is not None:
            vault[service] = {
                "website": new_url, 
                "username": new_user, 
                "password": new_pw, 
                "last_updated": datetime.now().strftime("%Y-%m-%d")
            }
            self.save_encrypted_vault(vault)
            self.refresh_data_grid()

    def copy_password_to_clipboard(self):
        """
        Copies password to clipboard with a 30-second security clear.
        """
        selection = self.data_grid.selection()
        if not selection:
            return
        service = self.data_grid.item(selection)['values'][0]
        vault = self.load_encrypted_vault()
        self.root.clipboard_clear()
        self.root.clipboard_append(vault[service]['password'])
        self.root.after(30000, lambda: self.root.clipboard_clear())

    def delete_vault_entry(self):
        """
        Removes an entry after user confirmation.
        """
        selection = self.data_grid.selection()
        if not selection:
            return
        service = self.data_grid.item(selection)['values'][0]
        if messagebox.askyesno("CONFIRM", f"DELETE {service}?", parent=self.root):
            vault = self.load_encrypted_vault()
            del vault[service]
            self.save_encrypted_vault(vault)
            self.refresh_data_grid()

if __name__ == "__main__":
    root_instance = tk.Tk()
    application = HackerVaultGUI(root_instance)
    root_instance.mainloop()