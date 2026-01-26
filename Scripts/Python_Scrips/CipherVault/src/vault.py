# Date: 2026-01-25
# Script Name: vault_hacker_gui.pyw
# Author: omegazyph
# Updated: 2026-01-26
# Description: AES-256 Vault with dual 2FA and On-Demand Generation.
# Features: Strict full-word naming, secrets-based security, and parent-locked focus.

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
        """
        Initializes the vault with dual 2FA support and strict full-word naming conventions.
        """
        self.root_window_instance = root_window_instance
        self.root_window_instance.title("SYSTEM_ACCESS: REDUNDANT_AUTH_VAULT_FINAL")
        
        # Wide geometry for dual 2FA columns on the Lenovo Legion display
        self.root_window_instance.geometry("1550x700")
        self.background_color_hex = "#000000"
        self.foreground_color_hex = "#00FF41" 
        self.font_style_standard = ("Courier New", 10, "bold")
        self.root_window_instance.configure(bg=self.background_color_hex)

        # Path Configuration
        script_path_absolute = os.path.abspath(__file__)
        script_directory_path = os.path.dirname(script_path_absolute)
        parent_directory_path = os.path.dirname(script_directory_path)
        
        self.data_directory_path = os.path.join(parent_directory_path, "data")
        self.backup_directory_path = os.path.join(self.data_directory_path, "backups")
        self.file_path_vault_binary = os.path.join(self.data_directory_path, "vault_data.bin")

        # Ensure directory structures exist
        if not os.path.exists(self.data_directory_path):
            os.makedirs(self.data_directory_path)
        if not os.path.exists(self.backup_directory_path):
            os.makedirs(self.backup_directory_path)

        # Secure Entry Focus for Master Key
        self.master_password_input_string = simpledialog.askstring(
            "SECURE_AUTHENTICATION", 
            "ENTER MASTER CRYPTOGRAPHIC KEY:", 
            show='*', 
            parent=self.root_window_instance
        )
        
        if not self.master_password_input_string:
            self.root_window_instance.destroy()
            return

        self.cryptographic_key_bytes = self.derive_cryptographic_key(self.master_password_input_string)
        self.cipher_engine_instance = Fernet(self.cryptographic_key_bytes)
        
        # Validate the key by attempting to load existing data
        if os.path.exists(self.file_path_vault_binary):
            decryption_test_result_data = self.load_encrypted_vault_data()
            if decryption_test_result_data is None:
                messagebox.showerror(
                    "ACCESS_DENIED", 
                    "INVALID MASTER KEY: DECRYPTION FAILED", 
                    parent=self.root_window_instance
                )
                self.root_window_instance.destroy()
                return

        self.setup_hacker_user_interface()

    def derive_cryptographic_key(self, password_input_string):
        """
        Derives a secure cryptographic key using PBKDF2HMAC.
        """
        static_salt_bytes = b'static_salt_for_omegazyph'
        key_derivation_function_instance = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=static_salt_bytes,
            iterations=100000,
        )
        derived_password_bytes = key_derivation_function_instance.derive(password_input_string.encode())
        return base64.urlsafe_b64encode(derived_password_bytes)

    def generate_secure_credential_string(self, length_integer=20, include_symbols_boolean=True):
        """
        Generates a random secure string using the secrets module.
        """
        character_pool_string = string.ascii_letters + string.digits
        if include_symbols_boolean:
            character_pool_string += "!@#$%^&*()-_=+"
        
        return "".join(secrets.choice(character_pool_string) for index_iterator in range(length_integer))

    def setup_hacker_user_interface(self):
        """
        Constructs the graphical user interface with full-word descriptions.
        """
        header_label_title_instance = tkinter_module.Label(
            self.root_window_instance, 
            text=">_ CIPHER_VAULT: REDUNDANT_AUTHENTICATION_STORAGE", 
            font=("Courier New", 16, "bold"), 
            bg=self.background_color_hex, 
            fg=self.foreground_color_hex
        )
        header_label_title_instance.pack(pady=15)

        # Interface Styling Configuration
        interface_style_instance = ttk.Style()
        interface_style_instance.theme_use("clam")
        interface_style_instance.configure(
            "Treeview", 
            background=self.background_color_hex, 
            foreground=self.foreground_color_hex, 
            fieldbackground=self.background_color_hex, 
            font=self.font_style_standard, 
            rowheight=30
        )
        interface_style_instance.map("Treeview", background=[('selected', '#003300')])
        interface_style_instance.configure(
            "Treeview.Heading", 
            background="#111111", 
            foreground=self.foreground_color_hex, 
            font=self.font_style_standard
        )

        # Columns with full English labels
        column_identifiers_tuple = (
            "Service", "Website", "Username", "Password", "PIN", 
            "Two_Factor_Primary", "Two_Factor_Secondary", "Last_Updated"
        )
        self.data_grid_view_instance = ttk.Treeview(self.root_window_instance, columns=column_identifiers_tuple, show='headings')
        
        for identifier_string in column_identifiers_tuple:
            self.data_grid_view_instance.heading(identifier_string, text=f"[ {identifier_string.upper()} ]")
            self.data_grid_view_instance.column(identifier_string, width=170, anchor=tkinter_module.CENTER)
            
        self.data_grid_view_instance.pack(pady=10, fill=tkinter_module.BOTH, expand=True, padx=25)

        # Navigation and Action Button Container
        button_container_frame_instance = tkinter_module.Frame(self.root_window_instance, bg=self.background_color_hex)
        button_container_frame_instance.pack(pady=20)
        
        button_configuration_dictionary = {
            "bg": "#111111", 
            "fg": self.foreground_color_hex, 
            "font": self.font_style_standard, 
            "width": 18, 
            "relief": "flat"
        }

        tkinter_module.Button(button_container_frame_instance, text="ADD_NEW_ENTRY", command=self.add_vault_entry, **button_configuration_dictionary).grid(row=0, column=0, padx=5)
        tkinter_module.Button(button_container_frame_instance, text="EDIT_ENTRY", command=self.edit_vault_entry, **button_configuration_dictionary).grid(row=0, column=1, padx=5)
        tkinter_module.Button(button_container_frame_instance, text="VIEW_ALL_DATA", command=self.view_vault_entry_details, **button_configuration_dictionary).grid(row=0, column=2, padx=5)
        tkinter_module.Button(button_container_frame_instance, text="GENERATE_PASS", command=self.copy_generated_credential_to_clipboard, **button_configuration_dictionary).grid(row=0, column=3, padx=5)
        tkinter_module.Button(button_container_frame_instance, text="OPEN_WEBSITE", command=self.open_associated_website, **button_configuration_dictionary).grid(row=0, column=4, padx=5)
        tkinter_module.Button(button_container_frame_instance, text="DELETE_ENTRY", command=self.delete_vault_entry, **button_configuration_dictionary).grid(row=0, column=5, padx=5)
        tkinter_module.Button(button_container_frame_instance, text="TERMINATE_VAULT", command=self.root_window_instance.destroy, **button_configuration_dictionary).grid(row=0, column=6, padx=5)

        self.refresh_data_grid_display()

    def load_encrypted_vault_data(self):
        """
        Reads and decrypts the vault database file using full-word logic.
        """
        if not os.path.exists(self.file_path_vault_binary):
            return {}
        try:
            with open(self.file_path_vault_binary, "rb") as file_reader_instance:
                encrypted_binary_data_blob = file_reader_instance.read()
                decrypted_json_bytes_data = self.cipher_engine_instance.decrypt(encrypted_binary_data_blob)
                return json.loads(decrypted_json_bytes_data.decode())
        except Exception:
            return None

    def save_encrypted_vault_data(self, vault_data_dictionary):
        """
        Encrypts and saves data to the vault and creates a backup file.
        """
        json_data_bytes_payload = json.dumps(vault_data_dictionary).encode()
        encrypted_data_output_blob = self.cipher_engine_instance.encrypt(json_data_bytes_payload)
        with open(self.file_path_vault_binary, "wb") as file_writer_instance:
            file_writer_instance.write(encrypted_data_output_blob)
            
        timestamp_string_identifier = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file_name_string = f"backup_{timestamp_string_identifier}.bin"
        shutil.copy2(self.file_path_vault_binary, os.path.join(self.backup_directory_path, backup_file_name_string))

    def refresh_data_grid_display(self):
        """
        Reloads the information from the vault into the visual treeview.
        """
        for existing_item_instance in self.data_grid_view_instance.get_children():
            self.data_grid_view_instance.delete(existing_item_instance)
            
        vault_information_dictionary = self.load_encrypted_vault_data()
        if vault_information_dictionary:
            for service_name_string in sorted(vault_information_dictionary.keys()):
                entry_data_dictionary = vault_information_dictionary[service_name_string]
                self.data_grid_view_instance.insert("", tkinter_module.END, values=(
                    service_name_string, 
                    entry_data_dictionary.get("website_address_string", "N/A"), 
                    entry_data_dictionary.get("username_string", "N/A"), 
                    "********", 
                    "****",     
                    "****",     
                    "****",     
                    entry_data_dictionary.get("last_updated_date_string", "UNKNOWN")
                ))

    def copy_generated_credential_to_clipboard(self):
        """
        Generates a password and puts it on clipboard for easy pasting into new entries.
        """
        newly_generated_password_string = self.generate_secure_credential_string(24)
        self.root_window_instance.clipboard_clear()
        self.root_window_instance.clipboard_append(newly_generated_password_string)
        messagebox.showinfo("GENERATOR", f"NEW SECURE PASSWORD COPIED:\n{newly_generated_password_string}", parent=self.root_window_instance)

    def add_vault_entry(self):
        """
        Prompts user for full entry details with auto-generation fallback.
        """
        service_name_input_string = simpledialog.askstring("INPUT_SERVICE", "ENTER SERVICE NAME:", parent=self.root_window_instance)
        if not service_name_input_string:
            return
            
        website_address_input_string = simpledialog.askstring("INPUT_URL", "ENTER WEBSITE URL:", parent=self.root_window_instance)
        username_input_string = simpledialog.askstring("INPUT_USERNAME", "ENTER USERNAME:", parent=self.root_window_instance)
        
        password_input_string = simpledialog.askstring("INPUT_PASSWORD", "ENTER PASSWORD (CANCEL FOR AUTO-GEN):", parent=self.root_window_instance)
        if password_input_string is None:
            password_input_string = self.generate_secure_credential_string(20)
            
        pin_code_input_string = simpledialog.askstring("INPUT_PIN", "ENTER PIN CODE (CANCEL FOR AUTO-GEN):", parent=self.root_window_instance)
        if pin_code_input_string is None:
            pin_code_input_string = self.generate_secure_credential_string(6, include_symbols_boolean=False)
            
        two_factor_primary_seed_string = simpledialog.askstring("INPUT_2FA_PRIMARY", "ENTER PRIMARY 2FA SEED:", parent=self.root_window_instance)
        two_factor_secondary_seed_string = simpledialog.askstring("INPUT_2FA_SECONDARY", "ENTER SECONDARY 2FA / BACKUP:", parent=self.root_window_instance)
            
        vault_dictionary_object = self.load_encrypted_vault_data()
        vault_dictionary_object[service_name_input_string] = {
            "website_address_string": website_address_input_string or "N/A", 
            "username_string": username_input_string or "N/A", 
            "password_string": password_input_string,
            "pin_code_string": pin_code_input_string,
            "two_factor_primary": two_factor_primary_seed_string or "N/A",
            "two_factor_secondary": two_factor_secondary_seed_string or "N/A",
            "last_updated_date_string": datetime.now().strftime("%Y-%m-%d")
        }
        self.save_encrypted_vault_data(vault_dictionary_object)
        self.refresh_data_grid_display()

    def edit_vault_entry(self):
        """
        Allows modification of any field for an existing entry.
        """
        current_selection_instance = self.data_grid_view_instance.selection()
        if not current_selection_instance:
            return
            
        service_identifier_string = self.data_grid_view_instance.item(current_selection_instance)['values'][0]
        vault_dictionary_object = self.load_encrypted_vault_data()
        entry_reference_dictionary = vault_dictionary_object[service_identifier_string]
        
        updated_website_string = simpledialog.askstring("EDIT_URL", "UPDATE URL:", initialvalue=entry_reference_dictionary.get("website_address_string"), parent=self.root_window_instance)
        updated_username_string = simpledialog.askstring("EDIT_USERNAME", "UPDATE USERNAME:", initialvalue=entry_reference_dictionary.get("username_string"), parent=self.root_window_instance)
        updated_password_string = simpledialog.askstring("EDIT_PASSWORD", "UPDATE PASSWORD:", initialvalue=entry_reference_dictionary.get("password_string"), parent=self.root_window_instance)
        updated_pin_string = simpledialog.askstring("EDIT_PIN", "UPDATE PIN:", initialvalue=entry_reference_dictionary.get("pin_code_string"), parent=self.root_window_instance)
        updated_two_factor_primary = simpledialog.askstring("EDIT_2FA_PRIMARY", "UPDATE 2FA PRIMARY:", initialvalue=entry_reference_dictionary.get("two_factor_primary"), parent=self.root_window_instance)
        updated_two_factor_secondary = simpledialog.askstring("EDIT_2FA_SECONDARY", "UPDATE 2FA SECONDARY:", initialvalue=entry_reference_dictionary.get("two_factor_secondary"), parent=self.root_window_instance)
        
        if updated_website_string is not None:
            vault_dictionary_object[service_identifier_string] = {
                "website_address_string": updated_website_string, 
                "username_string": updated_username_string, 
                "password_string": updated_password_string,
                "pin_code_string": updated_pin_string,
                "two_factor_primary": updated_two_factor_primary,
                "two_factor_secondary": updated_two_factor_secondary,
                "last_updated_date_string": datetime.now().strftime("%Y-%m-%d")
            }
            self.save_encrypted_vault_data(vault_dictionary_object)
            self.refresh_data_grid_display()

    def view_vault_entry_details(self):
        """
        Displays all decrypted security codes in a clear format.
        """
        current_selection_instance = self.data_grid_view_instance.selection()
        if not current_selection_instance:
            return
            
        service_identifier_string = self.data_grid_view_instance.item(current_selection_instance)['values'][0]
        vault_dictionary_object = self.load_encrypted_vault_data()
        entry_reference_dictionary = vault_dictionary_object[service_identifier_string]
        
        display_details_output_string = (
            f"SERVICE:           {service_identifier_string}\n"
            f"USERNAME:          {entry_reference_dictionary.get('username_string')}\n"
            f"PASSWORD:          {entry_reference_dictionary.get('password_string')}\n"
            f"PIN_CODE:          {entry_reference_dictionary.get('pin_code_string')}\n"
            f"PRIMARY_2FA:       {entry_reference_dictionary.get('two_factor_primary')}\n"
            f"SECONDARY_2FA:     {entry_reference_dictionary.get('two_factor_secondary')}"
        )
        messagebox.showinfo("DECRYPTED_VAULT_RECORD", display_details_output_string, parent=self.root_window_instance)

    def delete_vault_entry(self):
        """
        Removes the selected record from the database.
        """
        current_selection_instance = self.data_grid_view_instance.selection()
        if not current_selection_instance:
            return
            
        service_identifier_string = self.data_grid_view_instance.item(current_selection_instance)['values'][0]
        user_confirmation_boolean = messagebox.askyesno(
            "CONFIRM_DELETION", 
            f"ARE YOU SURE YOU WANT TO PERMANENTLY DELETE {service_identifier_string}?", 
            parent=self.root_window_instance
        )
        
        if user_confirmation_boolean:
            vault_dictionary_object = self.load_encrypted_vault_data()
            if service_identifier_string in vault_dictionary_object:
                del vault_dictionary_object[service_identifier_string]
                self.save_encrypted_vault_data(vault_dictionary_object)
                self.refresh_data_grid_display()

    def open_associated_website(self):
        """
        Launches the browser with the corrected protocol logic.
        """
        current_selection_instance = self.data_grid_view_instance.selection()
        if not current_selection_instance:
            return
            
        target_website_url_string = self.data_grid_view_instance.item(current_selection_instance)['values'][1]
        if target_website_url_string and target_website_url_string != "N/A":
            if not target_website_url_string.lower().startswith("http"):
                target_website_url_string = "https://" + target_website_url_string
            webbrowser.open(target_website_url_string)

if __name__ == "__main__":
    main_root_window_instance = tkinter_module.Tk()
    vault_application_class_instance = HackerVaultGUI(main_root_window_instance)
    main_root_window_instance.mainloop()