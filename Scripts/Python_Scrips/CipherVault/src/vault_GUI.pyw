# Date: 2026-01-25
# Script Name: vault_hacker_gui.pyw
# Author: omegazyph
# Updated: 2026-01-25
# Description: Stealth AES-256 Vault with Auto-Expanding Columns, Clipboard support, and Delete functionality.
# Features: Full non-shorthand logic, Windowless execution (.pyw), and Secure Clipboard timer.

import os
import json
import base64
import secrets
import string
import shutil
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
        Initializes the wide-view stealth GUI with high-contrast colors.
        """
        self.root = root
        self.root.title("SYSTEM_ACCESS: CIPHER_VAULT_PRO")
        
        # Hide the window during authentication
        self.root.withdraw()
        
        self.root.geometry("1150x650")
        self.bg_color = "#000000"
        self.fg_color = "#00FF41" 
        self.font_style = ("Courier New", 10, "bold")
        self.root.configure(bg=self.bg_color)

        # File Path Management
        script_path = os.path.abspath(__file__)
        script_dir = os.path.dirname(script_path)
        parent_dir = os.path.dirname(script_dir)
        
        self.data_dir = os.path.join(parent_dir, "data")
        self.backup_dir = os.path.join(self.data_dir, "backups")
        self.file_path = os.path.join(self.data_dir, "vault_data.bin")

        # Ensure directories exist
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

        # Authenticate User
        self.master_password = simpledialog.askstring("SECURE_AUTH", "ENTER MASTER KEY:", show='*')
        
        if self.master_password is None or self.master_password == "":
            self.root.destroy()
            return

        self.key = self._derive_key(self.master_password)
        self.cipher = Fernet(self.key)
        
        # Reveal window and build UI
        self.root.deiconify()
        self._setup_hacker_ui()

    def _derive_key(self, password):
        """
        Derives a cryptographic key using PBKDF2 with a static salt.
        """
        salt = b'static_salt_for_omegazyph'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        password_bytes = password.encode()
        key_bytes = kdf.derive(password_bytes)
        url_safe_key = base64.urlsafe_b64encode(key_bytes)
        return url_safe_key

    def _setup_hacker_ui(self):
        """
        Configures the grid, buttons, and status bar.
        """
        header = tk.Label(
            self.root, 
            text=">_ CIPHER_VAULT: PRO_EDITION_ACTIVE", 
            font=("Courier New", 16, "bold"), 
            bg=self.bg_color, 
            fg=self.fg_color
        )
        header.pack(pady=15)

        # Configure Treeview Style
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
        style.configure("Treeview.Heading", background="#111111", foreground=self.fg_color, font=self.font_style)

        tree_frame = tk.Frame(self.root, bg=self.bg_color)
        tree_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=25)

        # Define Columns
        columns = ("Service", "Website", "Username", "Last Updated")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        for column in columns:
            self.tree.heading(column, text=f"[ {column.upper()} ]")
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Vertical Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Control Panel
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(pady=20)
        
        button_settings = {
            "bg": "#111111", 
            "fg": self.fg_color, 
            "activebackground": self.fg_color, 
            "activeforeground": self.bg_color, 
            "font": self.font_style, 
            "width": 14, 
            "relief": "flat"
        }

        tk.Button(button_frame, text="ADD_NEW", command=self.add_entry, **button_settings).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="VIEW_DETAILS", command=self.view_entry, **button_settings).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="COPY_PASS", command=self.copy_password, **button_settings).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="DELETE_ENTRY", command=self.delete_entry, **button_settings).grid(row=0, column=3, padx=5)
        tk.Button(button_frame, text="REFRESH", command=self.refresh_list, **button_settings).grid(row=0, column=4, padx=5)
        tk.Button(button_frame, text="TERMINATE", command=self.root.destroy, **button_settings).grid(row=0, column=5, padx=5)

        # Interactive Status Bar
        self.status_var = tk.StringVar(value=f"SYSTEM_READY | VAULT: {self.file_path}")
        status_bar = tk.Label(
            self.root, 
            textvariable=self.status_var, 
            bd=1, 
            relief="sunken", 
            anchor="w",
            bg="#111111", 
            fg=self.fg_color, 
            font=("Courier New", 9)
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.refresh_list()

    def _auto_resize_columns(self):
        """
        Dynamically adjusts column widths based on the longest string in each column.
        """
        import tkinter.font as tkfont
        current_font = tkfont.Font(font=self.font_style)

        for column in self.tree["columns"]:
            # Start with header width
            header_text = f"[ {column.upper()} ]"
            max_width = current_font.measure(header_text) + 50
            
            for row_id in self.tree.get_children():
                cell_value = str(self.tree.set(row_id, column))
                cell_width = current_font.measure(cell_value) + 50
                if cell_width > max_width:
                    max_width = cell_width
            
            self.tree.column(column, width=max_width)

    def load_vault(self):
        """
        Decrypts the binary vault file and parses the JSON content.
        """
        if not os.path.exists(self.file_path):
            return {}
        
        try:
            with open(self.file_path, "rb") as vault_file:
                encrypted_content = vault_file.read()
                decrypted_bytes = self.cipher.decrypt(encrypted_content)
                json_string = decrypted_bytes.decode()
                return json.loads(json_string)
        except Exception:
            messagebox.showerror("ACCESS_DENIED", "AUTHENTICATION_FAILED: INVALID_MASTER_KEY")
            self.root.destroy()
            return None

    def refresh_list(self):
        """
        Clears the grid and repopulates it with the latest data from the vault.
        """
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        vault_data = self.load_vault()
        
        if vault_data is not None:
            for service_name in sorted(vault_data.keys()):
                entry = vault_data[service_name]
                self.tree.insert("", tk.END, values=(
                    service_name, 
                    entry.get("website", "N/A"), 
                    entry.get("username", "N/A"),
                    entry.get("last_updated", "UNKNOWN")
                ))
            self._auto_resize_columns()

    def add_entry(self):
        """
        Collects input via dialogs and saves a new record to the vault.
        """
        service = simpledialog.askstring("SYSTEM_INPUT", "TARGET_SERVICE:")
        if not service:
            return
        
        website = simpledialog.askstring("SYSTEM_INPUT", "TARGET_URL:")
        username = simpledialog.askstring("SYSTEM_INPUT", "IDENT_USER:")
        password = simpledialog.askstring("SYSTEM_INPUT", "SECRET_KEY (LEAVE BLANK FOR AUTO-GEN):")
        
        if not password:
            char_pool = string.ascii_letters + string.digits + "!@#$%^&*"
            password = "".join(secrets.choice(char_pool) for index in range(20))
            messagebox.showinfo("GEN_SUCCESS", f"KEY_GENERATED: {password}")

        vault_data = self.load_vault()
        if vault_data is not None:
            vault_data[service] = {
                "website": website if website else "N/A", 
                "username": username, 
                "password": password, 
                "last_updated": datetime.now().strftime("%Y-%m-%d")
            }
            self.save_vault(vault_data)
            self.refresh_list()

    def view_entry(self):
        """
        Displays all decrypted details for the selected entry in a popup.
        """
        selection = self.tree.selection()
        if not selection:
            return
            
        item_data = self.tree.item(selection)
        service_name = item_data['values'][0]
        
        vault_data = self.load_vault()
        if vault_data and service_name in vault_data:
            info = vault_data[service_name]
            details = (
                f"SERVICE:  {service_name}\n"
                f"ENDPOINT: {info.get('website')}\n"
                f"IDENTITY: {info.get('username')}\n"
                f"PASSWORD: {info.get('password')}"
            )
            messagebox.showinfo("DECRYPTED_RECORD", details)

    def copy_password(self):
        """
        Copies the password to the clipboard and triggers a 30-second security wipe.
        """
        selection = self.tree.selection()
        if not selection:
            return
            
        item_data = self.tree.item(selection)
        service_name = item_data['values'][0]
        
        vault_data = self.load_vault()
        if vault_data and service_name in vault_data:
            self.root.clipboard_clear()
            self.root.clipboard_append(vault_data[service_name]['password'])
            self.status_var.set("CLIPBOARD_STATUS: PASSWORD_COPIED (AUTO-CLEAR IN 30S)")
            self.root.after(30000, self._clear_clipboard)

    def _clear_clipboard(self):
        """
        Clears the clipboard to prevent accidental password leaks.
        """
        self.root.clipboard_clear()
        self.status_var.set(f"SYSTEM_READY | VAULT: {self.file_path}")

    def delete_entry(self):
        """
        Removes the selected record from the vault.
        """
        selection = self.tree.selection()
        if not selection:
            return
            
        item_data = self.tree.item(selection)
        service_name = item_data['values'][0]
        
        confirm = messagebox.askyesno("CONFIRM_ACTION", f"ARE YOU SURE YOU WANT TO DELETE {service_name}?")
        if confirm:
            vault_data = self.load_vault()
            if vault_data and service_name in vault_data:
                del vault_data[service_name]
                self.save_vault(vault_data)
                self.refresh_list()
                self.status_var.set(f"RECORD_DELETED: {service_name}")

    def save_vault(self, vault_data):
        """
        Encrypts the JSON data and saves it to a file, then creates a timestamped backup.
        """
        json_bytes = json.dumps(vault_data).encode()
        encrypted_bytes = self.cipher.encrypt(json_bytes)
        
        with open(self.file_path, "wb") as vault_file:
            vault_file.write(encrypted_bytes)
        
        # Backup Logic
        timestamp_string = datetime.now().strftime("%Y%m%d_%H%M%S")
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
            
        backup_filename = f"backup_{timestamp_string}.bin"
        backup_path = os.path.join(self.backup_dir, backup_filename)
        shutil.copy2(self.file_path, backup_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = HackerVaultGUI(root)
    root.mainloop()