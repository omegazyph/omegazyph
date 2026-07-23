# Date: 2026-01-25
# Script Name: vault_hacker_gui.py
# Author: omegazyph
# Updated: 2026-01-25
# Description: A Zero-Trust local password manager utilizing AES-256 encryption.
# Features: "Matrix" Hacker Aesthetic, Website Column support, 
# Automated binary backups, and full non-shorthand cryptographic logic.

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
        Initializes the GUI with a dark-mode hacker aesthetic.
        """
        self.root = root
        self.root.title("SYSTEM_ACCESS: CIPHER_VAULT_V2")
        self.root.geometry("850x500") # Widened to fit the Website column
        
        # Color Palette: Matrix Green and Deep Black
        self.bg_color = "#000000"
        self.fg_color = "#00FF41" 
        self.font_style = ("Courier New", 10, "bold")
        
        self.root.configure(bg=self.bg_color)

        # Setup paths
        script_path = os.path.abspath(__file__)
        script_dir = os.path.dirname(script_path)
        parent_dir = os.path.dirname(script_dir)
        
        self.data_dir = os.path.join(parent_dir, "data")
        self.backup_dir = os.path.join(self.data_dir, "backups")
        self.file_path = os.path.join(self.data_dir, "vault_data.bin")

        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

        # Immediate Auth
        self.master_password = simpledialog.askstring("ENCRYPTION_KEY", "ENTER MASTER KEY TO DECRYPT:", show='*')
        
        if not self.master_password:
            self.root.destroy()
            return

        self.key = self._derive_key(self.master_password)
        self.cipher = Fernet(self.key)
        
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
        Styles the GUI to look like a secure terminal with expanded columns.
        """
        header = tk.Label(
            self.root, 
            text=">_ CIPHER_VAULT: SECURE_SESSION_ACTIVE", 
            font=("Courier New", 14, "bold"),
            bg=self.bg_color, 
            fg=self.fg_color
        )
        header.pack(pady=10)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview", 
            background=self.bg_color, 
            foreground=self.fg_color, 
            fieldbackground=self.bg_color,
            font=self.font_style,
            rowheight=25
        )
        style.map("Treeview", background=[('selected', '#003300')])
        style.configure("Treeview.Heading", background="#111111", foreground=self.fg_color, font=self.font_style)

        tree_frame = tk.Frame(self.root, bg=self.bg_color)
        tree_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)

        # Added 'Website' to columns
        self.tree = ttk.Treeview(tree_frame, columns=("Service", "Website", "Username", "Status"), show='headings')
        self.tree.heading("Service", text="[ SERVICE_ID ]")
        self.tree.heading("Website", text="[ TARGET_URL ]")
        self.tree.heading("Username", text="[ USER_ID ]")
        self.tree.heading("Status", text="[ ENTROPY ]")
        
        # Set column widths
        self.tree.column("Service", width=150)
        self.tree.column("Website", width=250)
        self.tree.column("Username", width=150)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        btn_frame = tk.Frame(self.root, bg=self.bg_color)
        btn_frame.pack(pady=20)

        btn_style = {
            "bg": "#111111",
            "fg": self.fg_color,
            "activebackground": self.fg_color,
            "activeforeground": self.bg_color,
            "font": self.font_style,
            "bd": 1,
            "relief": "flat",
            "width": 15
        }

        tk.Button(btn_frame, text="ADD_ENTRY", command=self.add_entry, **btn_style).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="DECRYPT_INFO", command=self.view_entry, **btn_style).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="SYNC_VAULT", command=self.refresh_list, **btn_style).grid(row=0, column=2, padx=10)
        tk.Button(btn_frame, text="TERMINATE", command=self.root.destroy, **btn_style).grid(row=0, column=3, padx=10)

        self.refresh_list()

    def load_vault(self):
        """
        Decrypts the vault file with error handling.
        """
        if not os.path.exists(self.file_path):
            return {}
        try:
            with open(self.file_path, "rb") as vault_file:
                encrypted_data = vault_file.read()
                decrypted_data = self.cipher.decrypt(encrypted_data)
                return json.loads(decrypted_data.decode())
        except Exception:
            messagebox.showerror("ACCESS_DENIED", "AUTHENTICATION_FAILURE: INVALID_KEY")
            self.root.destroy()
            return None

    def refresh_list(self):
        """
        Populates the terminal list including website data.
        """
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        data = self.load_vault()
        if data:
            for svc in sorted(data.keys()):
                site = data[svc].get("website", "N/A")
                user = data[svc].get("username", "N/A")
                self.tree.insert("", tk.END, values=(svc, site, user, "ENCRYPTED"))

    def add_entry(self):
        """
        Hacker-style input prompts including website field.
        """
        service = simpledialog.askstring("SYS_INPUT", "TARGET_SERVICE:")
        if not service: 
            return
        
        website = simpledialog.askstring("SYS_INPUT", "TARGET_URL (N/A):")
        username = simpledialog.askstring("SYS_INPUT", "IDENT_USER:")
        password = simpledialog.askstring("SYS_INPUT", "SECRET_KEY (BLANK FOR AUTO-GEN):")
        
        if not password:
            alphabet = string.ascii_letters + string.digits + string.punctuation
            password = "".join(secrets.choice(alphabet) for _ in range(18))
            messagebox.showinfo("GEN_SUCCESS", f"KEY_GENERATED: {password}")

        data = self.load_vault()
        if data is not None:
            data[service] = {
                "website": website if website else "N/A",
                "username": username,
                "password": password,
                "last_updated": datetime.now().strftime("%Y-%m-%d")
            }
            self.save_vault(data)
            self.refresh_list()

    def view_entry(self):
        """
        Reveals all hidden info for the selected entry.
        """
        selected = self.tree.selection()
        if not selected:
            return
            
        item = self.tree.item(selected)
        svc_name = item['values'][0]
        
        data = self.load_vault()
        if data and svc_name in data:
            info = data[svc_name]
            details = (
                f"SERVICE: {svc_name}\n"
                f"URL:     {info.get('website', 'N/A')}\n"
                f"USER:    {info.get('username', 'N/A')}\n"
                f"PASS:    {info.get('password', 'N/A')}"
            )
            messagebox.showinfo("DECRYPTED_DATA", details)

    def save_vault(self, data):
        """
        Saves and generates an encrypted backup.
        """
        json_bytes = json.dumps(data).encode()
        encrypted_data = self.cipher.encrypt(json_bytes)
        with open(self.file_path, "wb") as vault_file:
            vault_file.write(encrypted_data)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(self.backup_dir, f"backup_{timestamp}.bin")
        shutil.copy2(self.file_path, backup_path)

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#000000")
    app = HackerVaultGUI(root)
    root.mainloop()