# Date: 2026-01-25
# Script Name: vault_hacker_gui.pyw
# Author: omegazyph
# Updated: 2026-01-26
# Description: Advanced Encryption Standard 256 Vault with four-digit numeric automatic generation.
# Features: Strict full-word naming conventions, expanded logic, and full-screen responsive layout.

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
        Initializes the vault with full-screen support and four-digit numeric generation.
        """
        self.root_window_instance = root_window_instance
        self.root_window_instance.title("SYSTEM_ACCESS: FULL_WORD_STRICT_VAULT")
        
        # Maximize the window for Windows 11 on the Lenovo Legion laptop
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

        # Create necessary directories if they do not exist
        if not os.path.exists(self.data_directory_path):
            os.makedirs(self.data_directory_path)
            
        if not os.path.exists(self.backup_directory_path):
            os.makedirs(self.backup_directory_path)

        # Master Key Authentication
        self.master_password_input_string = simpledialog.askstring(
            "SECURE_AUTHENTICATION", 
            "ENTER MASTER CRYPTOGRAPHIC KEY:", 
            show='*', 
            parent=self.root_window_instance
        )
        
        # Exit if no password is provided
        if not self.master_password_input_string:
            self.root_window_instance.destroy()
            return

        self.cryptographic_key_bytes = self.derive_cryptographic_key(self.master_password_input_string)
        self.cipher_engine_instance = Fernet(self.cryptographic_key_bytes)
        
        # Validate the master key if a vault file already exists
        if os.path.exists(self.file_path_vault_binary):
            vault_data_check = self.load_encrypted_vault_data()
            if vault_data_check is None:
                messagebox.showerror("ACCESS_DENIED", "INVALID MASTER KEY", parent=self.root_window_instance)
                self.root_window_instance.destroy()
                return

        self.setup_hacker_user_interface()

    def derive_cryptographic_key(self, password_input_string):
        """Derives a Fernet-compatible key using Password-Based Key Derivation Function 2."""
        static_salt_bytes = b'static_salt_for_omegazyph'
        
        key_derivation_function_instance = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=static_salt_bytes,
            iterations=100000,
        )
        
        password_bytes = password_input_string.encode()
        derived_key_bytes = key_derivation_function_instance.derive(password_bytes)
        
        return base64.urlsafe_b64encode(derived_key_bytes)

    def generate_secure_string(self, length_integer=20, mode_string="password"):
        """Generates either a complex password or a four-digit numeric personal identification number."""
        if mode_string == "personal_identification_number":
            character_pool_string = string.digits
            length_integer = 4
        else:
            character_pool_string = string.ascii_letters + string.digits + "!@#$%^&*"
            
        generated_characters_list = []
        for index_iterator in range(length_integer):
            random_character = secrets.choice(character_pool_string)
            generated_characters_list.append(random_character)
            
        return "".join(generated_characters_list)

    def setup_hacker_user_interface(self):
        """Builds the main graphical user interface with optimized columns."""
        header_label_title_instance = tkinter_module.Label(
            self.root_window_instance, 
            text=">_ CIPHER_VAULT: FULL_WORD_PROTOCOL_ACTIVE", 
            font=("Courier New", 14, "bold"), 
            bg=self.background_color_hexadecimal, 
            fg=self.foreground_color_hexadecimal
        )
        header_label_title_instance.pack(pady=10)

        tree_frame_instance = tkinter_module.Frame(self.root_window_instance, bg=self.background_color_hexadecimal)
        tree_frame_instance.pack(pady=10, fill=tkinter_module.BOTH, expand=True, padx=20)

        interface_style_instance = ttk.Style()
        interface_style_instance.theme_use("clam")
        interface_style_instance.configure(
            "Treeview", 
            background=self.background_color_hexadecimal, 
            foreground=self.foreground_color_hexadecimal, 
            fieldbackground=self.background_color_hexadecimal, 
            font=self.font_style_standard, 
            rowheight=25
        )
        interface_style_instance.map("Treeview", background=[('selected', '#003300')])

        self.column_identifiers_tuple = (
            "Service", 
            "Website_Address", 
            "Username", 
            "Password", 
            "Identification_Number", 
            "Two_Factor_Primary", 
            "Two_Factor_Secondary", 
            "Last_Updated"
        )
        self.data_grid_view_instance = ttk.Treeview(tree_frame_instance, columns=self.column_identifiers_tuple, show='headings')
        
        scrollbar_instance = ttk.Scrollbar(tree_frame_instance, orient="vertical", command=self.data_grid_view_instance.yview)
        self.data_grid_view_instance.configure(yscrollcommand=scrollbar_instance.set)
        
        column_settings_dictionary = {
            "Service": {"width": 200, "stretch": True},
            "Website_Address": {"width": 350, "stretch": True},
            "Username": {"width": 200, "stretch": True},
            "Password": {"width": 100, "stretch": False},
            "Identification_Number": {"width": 120, "stretch": False},
            "Two_Factor_Primary": {"width": 120, "stretch": False},
            "Two_Factor_Secondary": {"width": 120, "stretch": False},
            "Last_Updated": {"width": 120, "stretch": False}
        }

        for identifier_string in self.column_identifiers_tuple:
            self.data_grid_view_instance.heading(identifier_string, text=f"[ {identifier_string.upper()} ]")
            configuration = column_settings_dictionary.get(identifier_string)
            self.data_grid_view_instance.column(
                identifier_string, 
                width=configuration["width"], 
                anchor=tkinter_module.CENTER, 
                stretch=configuration["stretch"]
            )
            
        self.data_grid_view_instance.pack(side=tkinter_module.LEFT, fill=tkinter_module.BOTH, expand=True)
        scrollbar_instance.pack(side=tkinter_module.RIGHT, fill=tkinter_module.Y)

        button_container_frame_instance = tkinter_module.Frame(self.root_window_instance, bg=self.background_color_hexadecimal)
        button_container_frame_instance.pack(pady=20)
        
        button_configuration = {
            "bg": "#111111", 
            "fg": self.foreground_color_hexadecimal, 
            "font": self.font_style_standard, 
            "width": 25, 
            "relief": "flat"
        }

        tkinter_module.Button(button_container_frame_instance, text="ADD_NEW_ENTRY", command=self.add_vault_entry, **button_configuration).grid(row=0, column=0, padx=8)
        tkinter_module.Button(button_container_frame_instance, text="EDIT_EXISTING_ENTRY", command=self.edit_vault_entry, **button_configuration).grid(row=0, column=1, padx=8)
        tkinter_module.Button(button_container_frame_instance, text="VIEW_RECORD_DATA", command=self.view_vault_entry_details, **button_configuration).grid(row=0, column=2, padx=8)
        tkinter_module.Button(button_container_frame_instance, text="GENERATE_NEW_PASSWORD", command=self.copy_generated_credential_to_clipboard, **button_configuration).grid(row=0, column=3, padx=8)
        tkinter_module.Button(button_container_frame_instance, text="OPEN_WEBSITE_ADDRESS", command=self.open_associated_website, **button_configuration).grid(row=1, column=0, padx=8, pady=10)
        tkinter_module.Button(button_container_frame_instance, text="DELETE_ENTRY", command=self.delete_vault_entry, **button_configuration).grid(row=1, column=1, padx=8, pady=10)
        tkinter_module.Button(button_container_frame_instance, text="EXIT_APPLICATION", command=self.root_window_instance.destroy, **button_configuration).grid(row=1, column=2, padx=8, pady=10)

        self.refresh_data_grid_display()

    def load_encrypted_vault_data(self):
        """Loads and decrypts data from the binary vault file."""
        if not os.path.exists(self.file_path_vault_binary):
            return {}
            
        try:
            with open(self.file_path_vault_binary, "rb") as file_reader_instance:
                encrypted_content = file_reader_instance.read()
                
            decrypted_content_bytes = self.cipher_engine_instance.decrypt(encrypted_content)
            decrypted_content_string = decrypted_content_bytes.decode()
            
            return json.loads(decrypted_content_string)
        except Exception:
            return None

    def save_encrypted_vault_data(self, vault_data_dictionary):
        """Encrypts and saves data to the binary vault file and creates a backup."""
        json_data_string = json.dumps(vault_data_dictionary)
        json_data_bytes_payload = json_data_string.encode()
        
        encrypted_data_output_blob = self.cipher_engine_instance.encrypt(json_data_bytes_payload)
        
        with open(self.file_path_vault_binary, "wb") as file_writer_instance:
            file_writer_instance.write(encrypted_data_output_blob)
            
        current_time_object = datetime.now()
        timestamp_string_identifier = current_time_object.strftime("%Y%m%d_%H%M%S")
        
        backup_file_name = f"backup_{timestamp_string_identifier}.bin"
        backup_destination_path = os.path.join(self.backup_directory_path, backup_file_name)
        
        shutil.copy2(self.file_path_vault_binary, backup_destination_path)

    def refresh_data_grid_display(self):
        """Clears and repopulates the visual data grid."""
        for existing_item_instance in self.data_grid_view_instance.get_children():
            self.data_grid_view_instance.delete(existing_item_instance)
        
        vault_information_dictionary = self.load_encrypted_vault_data()
        
        if vault_information_dictionary:
            sorted_keys = sorted(vault_information_dictionary.keys())
            for service_name_string in sorted_keys:
                entry = vault_information_dictionary[service_name_string]
                
                website = entry.get("website_address_string") or "NOT_AVAILABLE"
                username = entry.get("username_string") or "NOT_AVAILABLE"
                last_updated = entry.get("last_updated_date_string") or "UNKNOWN"

                values_tuple = (service_name_string, website, username, "********", "****", "****", "****", last_updated)
                self.data_grid_view_instance.insert("", tkinter_module.END, values=values_tuple)

    def add_vault_entry(self):
        """Prompts for new entry details and saves them."""
        service_name_input_string = simpledialog.askstring("INPUT", "SERVICE NAME:", parent=self.root_window_instance)
        if not service_name_input_string:
            return
        
        website_address_input_string = simpledialog.askstring("INPUT", "WEBSITE ADDRESS:", parent=self.root_window_instance)
        username_input_string = simpledialog.askstring("INPUT", "USERNAME:", parent=self.root_window_instance)
        
        password_input_string = simpledialog.askstring("INPUT", "PASSWORD (CANCEL FOR AUTOMATIC):", parent=self.root_window_instance)
        if not password_input_string:
            password_input_string = self.generate_secure_string(20, "password")
            
        pin_code_input_string = simpledialog.askstring("INPUT", "PERSONAL IDENTIFICATION NUMBER (CANCEL FOR AUTOMATIC):", parent=self.root_window_instance)
        if not pin_code_input_string:
            pin_code_input_string = self.generate_secure_string(4, "personal_identification_number")
        
        two_factor_primary = simpledialog.askstring("INPUT", "TWO FACTOR PRIMARY:", parent=self.root_window_instance)
        two_factor_secondary = simpledialog.askstring("INPUT", "TWO FACTOR SECONDARY:", parent=self.root_window_instance)
            
        vault_dictionary_object = self.load_encrypted_vault_data()
        
        current_date_string = datetime.now().strftime("%Y-%m-%d")
        
        vault_dictionary_object[service_name_input_string] = {
            "website_address_string": website_address_input_string or "NOT_AVAILABLE", 
            "username_string": username_input_string or "NOT_AVAILABLE", 
            "password_string": password_input_string,
            "pin_code_string": pin_code_input_string,
            "two_factor_primary": two_factor_primary or "NOT_AVAILABLE",
            "two_factor_secondary": two_factor_secondary or "NOT_AVAILABLE",
            "last_updated_date_string": current_date_string
        }
        
        self.save_encrypted_vault_data(vault_dictionary_object)
        self.refresh_data_grid_display()

    def edit_vault_entry(self):
        """Allows modification of an existing entry."""
        current_selection_instance = self.data_grid_view_instance.selection()
        if not current_selection_instance:
            return
            
        selected_item = self.data_grid_view_instance.item(current_selection_instance)
        service_identifier_string = selected_item['values'][0]
        
        vault_dictionary_object = self.load_encrypted_vault_data()
        entry = vault_dictionary_object[service_identifier_string]
        
        initial_website = entry.get("website_address_string")
        initial_username = entry.get("username_string")
        initial_password = entry.get("password_string")
        initial_pin_code = entry.get("pin_code_string")
        initial_two_factor_primary = entry.get("two_factor_primary")
        initial_two_factor_secondary = entry.get("two_factor_secondary")

        updated_website = simpledialog.askstring("EDIT", "WEBSITE ADDRESS:", initialvalue=initial_website, parent=self.root_window_instance)
        updated_username = simpledialog.askstring("EDIT", "USERNAME:", initialvalue=initial_username, parent=self.root_window_instance)
        
        updated_password = simpledialog.askstring("EDIT", "PASSWORD (CLEAR FOR AUTOMATIC):", initialvalue=initial_password, parent=self.root_window_instance)
        if not updated_password:
            updated_password = self.generate_secure_string(20, "password")
        
        updated_pin_code = simpledialog.askstring("EDIT", "PERSONAL IDENTIFICATION NUMBER (CLEAR FOR AUTOMATIC):", initialvalue=initial_pin_code, parent=self.root_window_instance)
        if not updated_pin_code:
            updated_pin_code = self.generate_secure_string(4, "personal_identification_number")

        updated_two_factor_primary = simpledialog.askstring("EDIT", "TWO FACTOR PRIMARY:", initialvalue=initial_two_factor_primary, parent=self.root_window_instance)
        updated_two_factor_secondary = simpledialog.askstring("EDIT", "TWO FACTOR SECONDARY:", initialvalue=initial_two_factor_secondary, parent=self.root_window_instance)
        
        if updated_website is not None:
            current_date_string = datetime.now().strftime("%Y-%m-%d")
            
            vault_dictionary_object[service_identifier_string] = {
                "website_address_string": updated_website, 
                "username_string": updated_username, 
                "password_string": updated_password, 
                "pin_code_string": updated_pin_code,
                "two_factor_primary": updated_two_factor_primary, 
                "two_factor_secondary": updated_two_factor_secondary,
                "last_updated_date_string": current_date_string
            }
            self.save_encrypted_vault_data(vault_dictionary_object)
            self.refresh_data_grid_display()

    def view_vault_entry_details(self):
        """Displays all details for the selected record in a pop-up window."""
        current_selection_instance = self.data_grid_view_instance.selection()
        if not current_selection_instance:
            return
            
        selected_item = self.data_grid_view_instance.item(current_selection_instance)
        service_identifier_string = selected_item['values'][0]
        
        vault_dictionary_object = self.load_encrypted_vault_data()
        entry = vault_dictionary_object[service_identifier_string]
        
        message_lines_list = []
        message_lines_list.append(f"SERVICE:                     {service_identifier_string}")
        message_lines_list.append(f"USERNAME:                    {entry.get('username_string')}")
        message_lines_list.append(f"PASSWORD:                    {entry.get('password_string')}")
        message_lines_list.append(f"IDENTIFICATION_NUMBER:       {entry.get('pin_code_string')}")
        message_lines_list.append(f"TWO_FACTOR_PRIMARY:          {entry.get('two_factor_primary')}")
        message_lines_list.append(f"TWO_FACTOR_SECONDARY:        {entry.get('two_factor_secondary')}")
        message_lines_list.append(f"DATE_LAST_UPDATED:           {entry.get('last_updated_date_string')}")
        
        display_string = "\n".join(message_lines_list)
        messagebox.showinfo("RECORD_DETAILS", display_string, parent=self.root_window_instance)

    def delete_vault_entry(self):
        """Deletes the selected entry from the vault after confirmation."""
        current_selection_instance = self.data_grid_view_instance.selection()
        if not current_selection_instance:
            return
            
        selected_item = self.data_grid_view_instance.item(current_selection_instance)
        service_identifier_string = selected_item['values'][0]
        
        confirmation_message = f"ARE YOU CERTAIN YOU WANT TO DELETE {service_identifier_string}?"
        if messagebox.askyesno("CONFIRMATION", confirmation_message, parent=self.root_window_instance):
            vault_dictionary_object = self.load_encrypted_vault_data()
            if service_identifier_string in vault_dictionary_object:
                del vault_dictionary_object[service_identifier_string]
                self.save_encrypted_vault_data(vault_dictionary_object)
                self.refresh_data_grid_display()

    def open_associated_website(self):
        """Opens the stored website address in the default web browser."""
        current_selection_instance = self.data_grid_view_instance.selection()
        if not current_selection_instance:
            return
            
        selected_item = self.data_grid_view_instance.item(current_selection_instance)
        target_website_address = selected_item['values'][1]
        
        if target_website_address and target_website_address != "NOT_AVAILABLE":
            if not target_website_address.lower().startswith("http"):
                target_website_address = "https://" + target_website_address
            webbrowser.open(target_website_address)

    def copy_generated_credential_to_clipboard(self):
        """Generates a high-security password and copies it to the system clipboard."""
        new_password = self.generate_secure_string(24, "password")
        self.root_window_instance.clipboard_clear()
        self.root_window_instance.clipboard_append(new_password)
        messagebox.showinfo("GENERATOR", "NEW PASSWORD COPIED TO CLIPBOARD.", parent=self.root_window_instance)

if __name__ == "__main__":
    main_root_window_instance = tkinter_module.Tk()
    vault_application_class_instance = HackerVaultGUI(main_root_window_instance)
    main_root_window_instance.mainloop()