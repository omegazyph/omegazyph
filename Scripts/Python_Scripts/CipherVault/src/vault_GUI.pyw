# Date: 2026-01-25
# Script Name: vault_hacker_gui.pyw
# Author: omegazyph
# Updated: 2026-01-26
# Description: AES-256 Vault with PIN_NUMBER labeling and legacy key support.
# Features: Corrects data storage mismatch by checking for multiple key variations.

import os
import json
import base64
import shutil
import webbrowser
import secrets
import string
import tkinter as tkinter_module
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime

# Cryptography imports
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

class HackerVaultGUI:
    def __init__(self, root_window_instance):
        """Initializes the vault and ensures all dialogs stay in the foreground."""
        self.root_window_instance = root_window_instance
        self.root_window_instance.title("Omegazyph Password Manager")
        self.root_window_instance.state('zoomed')
        
        self.background_color_hexadecimal = "#000000"
        self.foreground_color_hexadecimal = "#00FF41" 
        self.font_style_standard = ("Courier New", 10, "bold")
        self.root_window_instance.configure(bg=self.background_color_hexadecimal)

        # Path Configuration
        script_path_absolute = os.path.abspath(__file__)
        script_directory_path = os.path.dirname(script_path_absolute)
        parent_directory_path = os.path.dirname(script_directory_path)
        
        self.data_directory_path = os.path.join(parent_directory_path, "data")
        self.backup_directory_path = os.path.join(self.data_directory_path, "backups")
        self.file_path_vault_binary = os.path.join(self.data_directory_path, "vault_data.bin")

        if os.path.exists(self.data_directory_path) is False:
            os.makedirs(self.data_directory_path)

        if os.path.exists(self.backup_directory_path) is False:
            os.makedirs(self.backup_directory_path)

        # Master Key Authentication
        self.master_password_input_string = simpledialog.askstring(
            "SECURE_AUTHENTICATION", 
            "Password", 
            show='*', 
            parent=self.root_window_instance
        )
        
        if self.master_password_input_string is None:
            self.root_window_instance.destroy()
            return

        self.cryptographic_key_bytes = self.derive_cryptographic_key(self.master_password_input_string)
        self.cipher_engine_instance = Fernet(self.cryptographic_key_bytes)
        
        if os.path.exists(self.file_path_vault_binary) is True:
            decrypted_data_test = self.load_encrypted_vault_data()
            if decrypted_data_test is None:
                messagebox.showerror("ACCESS_DENIED", "INVALID Password", parent=self.root_window_instance)
                self.root_window_instance.destroy()
                return

        self.setup_hacker_user_interface()

    def derive_cryptographic_key(self, password_input_string):
        """Derives a Fernet key using PBKDF2 with a static salt."""
        static_salt_bytes = b'static_salt_for_omegazyph'
        key_derivation_function_instance = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=static_salt_bytes,
            iterations=100000,
        )
        derived_key_bytes = key_derivation_function_instance.derive(password_input_string.encode())
        return base64.urlsafe_b64encode(derived_key_bytes)

    def generate_secure_string(self, length_integer=20, mode_string="password"):
        """Generates complex passwords or 4-digit identification numbers."""
        if mode_string == "personal_identification_number":
            character_pool_string = string.digits
            length_integer = 4
        else:
            character_pool_string = string.ascii_letters + string.digits + "!@#$%^&*"
            
        generated_list = []
        for index in range(length_integer):
            random_character = secrets.choice(character_pool_string)
            generated_list.append(random_character)
            
        final_string = "".join(generated_list)
        return final_string

    def setup_hacker_user_interface(self):
        """Builds the main dashboard with PIN_NUMBER headers."""
        header_label = tkinter_module.Label(
            self.root_window_instance, 
            text=">_Password_Manager_Ready", 
            font=("Courier New", 14, "bold"), 
            bg=self.background_color_hexadecimal, 
            fg=self.foreground_color_hexadecimal
        )
        header_label.pack(pady=10)

        tree_frame = tkinter_module.Frame(self.root_window_instance, bg=self.background_color_hexadecimal)
        tree_frame.pack(pady=10, fill=tkinter_module.BOTH, expand=True, padx=20)

        style_instance = ttk.Style()
        style_instance.theme_use("clam")
        style_instance.configure(
            "Treeview", 
            background="#000000", 
            foreground="#00FF41", 
            fieldbackground="#000000", 
            font=self.font_style_standard
        )
        style_instance.map("Treeview", background=[('selected', '#004400')])

        self.column_identifiers = ("Service", "Website", "Username", "Password", "PIN_Number", "Date_Updated")
        self.data_grid_view_instance = ttk.Treeview(tree_frame, columns=self.column_identifiers, show='headings')

        column_widths_dictionary = {
            "Service": 150, 
            "Website": 280, 
            "Username": 180, 
            "Password": 100, 
            "PIN_Number": 100, 
            "Date_Updated": 150
        }
        
        for identifier in self.column_identifiers:
            self.data_grid_view_instance.heading(identifier, text=f"[ {identifier.upper()} ]")
            self.data_grid_view_instance.column(identifier, width=column_widths_dictionary[identifier], anchor="center")

        self.data_grid_view_instance.pack(side="left", fill="both", expand=True)

        button_frame = tkinter_module.Frame(self.root_window_instance, bg=self.background_color_hexadecimal)
        button_frame.pack(pady=20)
        
        button_style_dictionary = {
            "bg": "#111111", 
            "fg": "#00FF41", 
            "font": self.font_style_standard, 
            "width": 18, 
            "relief": "flat"
        }

        # Control Panel
        add_button = tkinter_module.Button(button_frame, text="ADD_NEW_ENTRY", command=self.add_vault_entry, **button_style_dictionary)
        add_button.grid(row=0, column=0, padx=5, pady=5)
        
        edit_button = tkinter_module.Button(button_frame, text="EDIT_ENTRY", command=self.edit_vault_entry, **button_style_dictionary)
        edit_button.grid(row=0, column=1, padx=5, pady=5)
        
        view_button = tkinter_module.Button(button_frame, text="VIEW_DATA", command=self.view_vault_entry_details, **button_style_dictionary)
        view_button.grid(row=0, column=2, padx=5, pady=5)
        
        open_button = tkinter_module.Button(button_frame, text="OPEN_WEBSITE", command=self.open_associated_website, **button_style_dictionary)
        open_button.grid(row=0, column=3, padx=5, pady=5)
        
        delete_button = tkinter_module.Button(button_frame, text="DELETE_ENTRY", command=self.delete_vault_entry, **button_style_dictionary)
        delete_button.grid(row=0, column=4, padx=5, pady=5)

        # Action Panel
        copy_pass_button = tkinter_module.Button(button_frame, text="COPY_PASSWORD", command=self.copy_password, **button_style_dictionary)
        copy_pass_button.grid(row=1, column=1, padx=5, pady=5)
        
        copy_pin_button = tkinter_module.Button(button_frame, text="COPY_PIN_NUMBER", command=self.copy_identification_number, **button_style_dictionary)
        copy_pin_button.grid(row=1, column=2, padx=5, pady=5)
        
        exit_button = tkinter_module.Button(button_frame, text="EXIT_SYSTEM", command=self.root_window_instance.destroy, **button_style_dictionary)
        exit_button.grid(row=1, column=3, padx=5, pady=5)

        self.refresh_data_grid_display()

    def load_encrypted_vault_data(self):
        """Decrypts and returns the vault data dictionary."""
        if os.path.exists(self.file_path_vault_binary) is False:
            return {}
        try:
            with open(self.file_path_vault_binary, "rb") as binary_file_reader:
                encrypted_content = binary_file_reader.read()
                decrypted_bytes = self.cipher_engine_instance.decrypt(encrypted_content)
                decrypted_string = decrypted_bytes.decode()
                return json.loads(decrypted_string)
        except Exception:
            return None

    def save_encrypted_vault_data(self, vault_dictionary):
        """Saves encrypted data and creates a physical backup."""
        json_string = json.dumps(vault_dictionary)
        json_bytes = json_string.encode()
        encrypted_blob = self.cipher_engine_instance.encrypt(json_bytes)
        
        with open(self.file_path_vault_binary, "wb") as binary_file_writer:
            binary_file_writer.write(encrypted_blob)
            
        timestamp_string = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file_name = f"backup_{timestamp_string}.bin"
        backup_destination_path = os.path.join(self.backup_directory_path, backup_file_name)
        shutil.copy2(self.file_path_vault_binary, backup_destination_path)

    def refresh_data_grid_display(self):
        """Updates the visual grid with support for old ID_NUMBER keys."""
        for existing_item in self.data_grid_view_instance.get_children():
            self.data_grid_view_instance.delete(existing_item)
            
        vault_data_dictionary = self.load_encrypted_vault_data()
        
        if vault_data_dictionary is not None:
            sorted_service_keys = sorted(vault_data_dictionary.keys())
            for service_name in sorted_service_keys:
                entry_data = vault_data_dictionary[service_name]
                
                website_value = entry_data.get("website_address_string") or entry_data.get("website") or "N/A"
                username_value = entry_data.get("username_string") or entry_data.get("username") or "N/A"
                date_value = entry_data.get("last_updated_date_string") or entry_data.get("last_updated") or "UNKNOWN"
                
                display_values = (service_name, website_value, username_value, "********", "****", date_value)
                self.data_grid_view_instance.insert("", "end", values=display_values)

    def copy_password(self):
        """Copies password to clipboard."""
        selected_item = self.data_grid_view_instance.selection()
        if not selected_item:
            return
            
        service_name = self.data_grid_view_instance.item(selected_item)['values'][0]
        vault_data = self.load_encrypted_vault_data()
        password_value = vault_data[service_name].get("password_string") or vault_data[service_name].get("password")
        
        self.root_window_instance.clipboard_clear()
        self.root_window_instance.clipboard_append(password_value)
        messagebox.showinfo("SUCCESS", f"PASSWORD FOR {service_name} COPIED.", parent=self.root_window_instance)

    def copy_identification_number(self):
        """Copies PIN_NUMBER to clipboard with legacy fallback."""
        selected_item = self.data_grid_view_instance.selection()
        if not selected_item:
            return
            
        service_name = self.data_grid_view_instance.item(selected_item)['values'][0]
        vault_data = self.load_encrypted_vault_data()
        entry = vault_data[service_name]
        
        # Checking for PIN first, then falling back to ID if it exists
        pin_value = entry.get("pin_code_string") or entry.get("id_number_string") or entry.get("pin")
        
        self.root_window_instance.clipboard_clear()
        self.root_window_instance.clipboard_append(pin_value)
        messagebox.showinfo("SUCCESS", f"PIN_NUMBER FOR {service_name} COPIED.", parent=self.root_window_instance)

    def add_vault_entry(self):
        """Captures and stores new entries."""
        service_name = simpledialog.askstring("INPUT", "SERVICE NAME:", parent=self.root_window_instance)
        if not service_name:
            return
            
        website_address = simpledialog.askstring("INPUT", "WEBSITE ADDRESS:", parent=self.root_window_instance)
        user_name = simpledialog.askstring("INPUT", "USERNAME:", parent=self.root_window_instance)
        
        password_input = simpledialog.askstring("INPUT", "PASSWORD (CANCEL FOR AUTO):", parent=self.root_window_instance)
        if not password_input:
            password_input = self.generate_secure_string(20, "password")
            
        pin_input = simpledialog.askstring("INPUT", "PIN_NUMBER (CANCEL FOR AUTO):", parent=self.root_window_instance)
        if not pin_input:
            pin_input = self.generate_secure_string(4, "personal_identification_number")

        fa_primary_input = simpledialog.askstring("INPUT", "2FA PRIMARY CODE (IF ANY):", parent=self.root_window_instance)
        fa_secondary_input = simpledialog.askstring("INPUT", "2FA SECONDARY CODE (IF ANY):", parent=self.root_window_instance)
        
        vault_data = self.load_encrypted_vault_data()
        current_date_string = datetime.now().strftime("%Y-%m-%d")
        
        vault_data[service_name] = {
            "website_address_string": website_address or "N/A", 
            "username_string": user_name or "N/A",
            "password_string": password_input, 
            "pin_code_string": pin_input,
            "two_factor_primary": fa_primary_input or "N/A", 
            "two_factor_secondary": fa_secondary_input or "N/A",
            "last_updated_date_string": current_date_string
        }
        
        self.save_encrypted_vault_data(vault_data)
        self.refresh_data_grid_display()

    def edit_vault_entry(self):
        """Edits entries while maintaining legacy key safety."""
        selected_item = self.data_grid_view_instance.selection()
        if not selected_item:
            return
            
        service_name = self.data_grid_view_instance.item(selected_item)['values'][0]
        vault_data = self.load_encrypted_vault_data()
        existing_entry = vault_data[service_name]

        current_web = existing_entry.get("website_address_string") or existing_entry.get("website")
        current_user = existing_entry.get("username_string") or existing_entry.get("username")
        current_pass = existing_entry.get("password_string") or existing_entry.get("password")
        # Legacy search for PIN
        current_pin = existing_entry.get("pin_code_string") or existing_entry.get("id_number_string") or "N/A"
        current_2fa_1 = existing_entry.get("two_factor_primary") or "N/A"
        current_2fa_2 = existing_entry.get("two_factor_secondary") or "N/A"

        new_web = simpledialog.askstring("EDIT", "WEBSITE ADDRESS:", initialvalue=current_web, parent=self.root_window_instance)
        new_user = simpledialog.askstring("EDIT", "USERNAME:", initialvalue=current_user, parent=self.root_window_instance)
        new_pass = simpledialog.askstring("EDIT", "PASSWORD:", initialvalue=current_pass, parent=self.root_window_instance)
        new_pin = simpledialog.askstring("EDIT", "PIN_NUMBER:", initialvalue=current_pin, parent=self.root_window_instance)
        new_2fa_1 = simpledialog.askstring("EDIT", "2FA PRIMARY:", initialvalue=current_2fa_1, parent=self.root_window_instance)
        new_2fa_2 = simpledialog.askstring("EDIT", "2FA SECONDARY:", initialvalue=current_2fa_2, parent=self.root_window_instance)

        if new_web is not None:
            current_date_string = datetime.now().strftime("%Y-%m-%d")
            vault_data[service_name] = {
                "website_address_string": new_web, 
                "username_string": new_user,
                "password_string": new_pass, 
                "pin_code_string": new_pin,
                "two_factor_primary": new_2fa_1 or "N/A",
                "two_factor_secondary": new_2fa_2 or "N/A",
                "last_updated_date_string": current_date_string
            }
            self.save_encrypted_vault_data(vault_data)
            self.refresh_data_grid_display()

    def view_vault_entry_details(self):
        """Displays full details with PIN_NUMBER label and legacy check."""
        selected_item = self.data_grid_view_instance.selection()
        if not selected_item:
            return
            
        service_name = self.data_grid_view_instance.item(selected_item)['values'][0]
        vault_data = self.load_encrypted_vault_data()
        entry_data = vault_data[service_name]
        
        web_value = entry_data.get('website_address_string') or entry_data.get('website')
        user_value = entry_data.get('username_string') or entry_data.get('username')
        pass_value = entry_data.get('password_string') or entry_data.get('password')
        # Legacy search for display
        pin_value = entry_data.get('pin_code_string') or entry_data.get('id_number_string') or 'N/A'
        fa_1_value = entry_data.get('two_factor_primary') or 'N/A'
        fa_2_value = entry_data.get('two_factor_secondary') or 'N/A'
        date_value = entry_data.get('last_updated_date_string') or 'UNKNOWN'
        
        details_text = (
            f"SERVICE:       {service_name}\n"
            f"WEBSITE:       {web_value}\n"
            f"USERNAME:      {user_value}\n"
            f"PASSWORD:      {pass_value}\n"
            f"PIN_NUMBER:    {pin_value}\n"
            f"2FA_PRIMARY:   {fa_1_value}\n"
            f"2FA_SECONDARY: {fa_2_value}\n"
            f"DATE_UPDATED:  {date_value}"
        )
        messagebox.showinfo("RECORD_DETAILS", details_text, parent=self.root_window_instance)

    def open_associated_website(self):
        """Opens URL in browser."""
        selected_item = self.data_grid_view_instance.selection()
        if not selected_item:
            return
        url_address = self.data_grid_view_instance.item(selected_item)['values'][1]
        if url_address and url_address != "N/A":
            if url_address.startswith("http") is False:
                url_address = "https://" + url_address
            webbrowser.open(url_address)

    def delete_vault_entry(self):
        """Removes entry after confirmation."""
        selected_item = self.data_grid_view_instance.selection()
        if not selected_item:
            return
        service_name = self.data_grid_view_instance.item(selected_item)['values'][0]
        confirm_deletion = messagebox.askyesno("CONFIRM", f"DELETE {service_name}?", parent=self.root_window_instance)
        if confirm_deletion is True:
            vault_data = self.load_encrypted_vault_data()
            if service_name in vault_data:
                del vault_data[service_name]
                self.save_encrypted_vault_data(vault_data)
                self.refresh_data_grid_display()

if __name__ == "__main__":
    root_window_object = tkinter_module.Tk()
    app_instance = HackerVaultGUI(root_window_object)
    root_window_object.mainloop()