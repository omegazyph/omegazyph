# Date: 2026-01-25
# Script Name: vault.py
# Author: omegazyph
# Updated: 2026-01-25
# Description: A Zero-Trust local password manager utilizing AES-256 encryption.
# Features: Full non-shorthand code, Universal 'exit' support, 
# Dynamic window auto-sizing, and Password Generation support during Updates.

import os
import json
import base64
import secrets
import string
import shutil
from datetime import datetime

# Cryptography imports
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

# Rich UI imports
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

# Initialize Rich console
console = Console()

class CipherVault:
    def __init__(self, master_password):
        """
        Initializes pathing and creates necessary data/backup directories.
        """
        script_path = os.path.abspath(__file__)
        script_dir = os.path.dirname(script_path)
        parent_dir = os.path.dirname(script_dir)
        
        # Folder structure logic
        self.data_dir = os.path.join(parent_dir, "data")
        self.backup_dir = os.path.join(self.data_dir, "backups")
        self.file_path = os.path.join(self.data_dir, "vault_data.bin")
        
        # Creating folders if they do not exist using 'not' checks
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

        self.key = self._derive_key(master_password)
        self.cipher = Fernet(self.key)
        self.expiration_days = 90

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

    def _create_backup(self):
        """
        Creates a timestamped backup of the encrypted binary file.
        """
        if os.path.exists(self.file_path):
            current_time = datetime.now()
            timestamp = current_time.strftime("%Y%m%d_%H%M%S")
            backup_name = "backup_" + timestamp + ".bin"
            backup_path = os.path.join(self.backup_dir, backup_name)
            shutil.copy2(self.file_path, backup_path)
            console.print("[dim cyan]System: Auto-backup complete (" + backup_name + ")[/dim cyan]")

    def load_vault(self):
        """
        Decrypts the vault file and returns the data as a dictionary.
        """
        if not os.path.exists(self.file_path):
            return {}
        try:
            with open(self.file_path, "rb") as vault_file:
                encrypted_data = vault_file.read()
                decrypted_data = self.cipher.decrypt(encrypted_data)
                vault_json = decrypted_data.decode()
                vault_dict = json.loads(vault_json)
                return vault_dict
        except Exception:
            console.print("[bold red]ERROR:[/bold red] Authentication failed.")
            return None

    def save_vault(self, data):
        """
        Encrypts and saves the data dictionary.
        """
        json_string = json.dumps(data)
        json_bytes = json_string.encode()
        encrypted_data = self.cipher.encrypt(json_bytes)
        with open(self.file_path, "wb") as vault_file:
            vault_file.write(encrypted_data)
        self._create_backup()

    def generate_password(self):
        """
        Generates an 18-character secure random password.
        """
        length = 18
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password_chars = []
        for i in range(length):
            char = secrets.choice(alphabet)
            password_chars.append(char)
        secure_password = "".join(password_chars)
        return secure_password

    def update_entry(self):
        """
        Allows field updates with 'exit' checks and password generation support.
        """
        service_name = Prompt.ask("Service to Update (or 'exit')")
        if service_name.lower() == "exit":
            return

        data = self.load_vault()
        if data is not None:
            if service_name in data:
                console.print("\n[bold cyan]Editing: " + service_name + "[/bold cyan]")
                console.print("1. Website  2. Username  3. Password  4. PIN  5. Cancel")
                field_choice = Prompt.ask("Select field", choices=["1", "2", "3", "4", "5"])
                
                if field_choice == "5":
                    return

                # Special logic for Password field (Option 3)
                if field_choice == "3":
                    gen_confirm = Prompt.ask("Generate a new password?", choices=["y", "n", "exit"], default="y")
                    if gen_confirm.lower() == "exit":
                        return
                    
                    if gen_confirm == "y":
                        new_val = self.generate_password()
                        console.print("\n[bold yellow]NEW GENERATED PASSWORD:[/bold yellow] " + new_val + "\n")
                    else:
                        new_val = Prompt.ask("Enter new Password (or 'exit')", password=True)
                        if new_val.lower() == "exit":
                            return
                else:
                    # Standard logic for other fields
                    new_val = Prompt.ask("Enter new value (or 'exit')")
                    if new_val.lower() == "exit":
                        return

                # Update the specific field
                if field_choice == "1":
                    data[service_name]["website"] = new_val
                elif field_choice == "2":
                    data[service_name]["username"] = new_val
                elif field_choice == "3":
                    data[service_name]["password"] = new_val
                elif field_choice == "4":
                    data[service_name]["pin"] = new_val

                data[service_name]["last_updated"] = datetime.now().strftime("%Y-%m-%d")
                self.save_vault(data)
                console.print("[bold green][*][/bold green] Update saved.")
            else:
                console.print("[red]Service not found.[/red]")

    def add_password(self):
        """
        Adds a new entry with full exit support.
        """
        service = Prompt.ask("Service (or 'exit')")
        if service.lower() == "exit":
            return

        site = Prompt.ask("Website (or 'exit')", default="N/A")
        if site.lower() == "exit":
            return

        user = Prompt.ask("Username (or 'exit')")
        if user.lower() == "exit":
            return

        pin = Prompt.ask("PIN (or 'exit')", default="N/A")
        if pin.lower() == "exit":
            return

        gen_confirm = Prompt.ask("Generate password?", choices=["y", "n", "exit"], default="y")
        if gen_confirm.lower() == "exit":
            return
        
        if gen_confirm == "y":
            pwd = self.generate_password()
            console.print("\n[bold yellow]GENERATED:[/bold yellow] " + pwd + "\n")
        else:
            pwd = Prompt.ask("Password (or 'exit')", password=True)
            if pwd.lower() == "exit":
                return

        data = self.load_vault()
        if data is not None:
            data[service] = {
                "username": user,
                "password": pwd,
                "website": site,
                "pin": pin,
                "last_updated": datetime.now().strftime("%Y-%m-%d")
            }
            self.save_vault(data)
            console.print("[bold green][+][/bold green] Entry secured.")

    def search_entries(self):
        """
        Searches the vault with an exit option.
        """
        query = Prompt.ask("Keyword (or 'exit')")
        if query.lower() == "exit":
            return

        data = self.load_vault()
        if data is None: 
            return
            
        table = Table(title="Results: " + query, border_style="blue", show_lines=True, width=console.width)
        table.add_column("Service", style="cyan", no_wrap=True)
        table.add_column("Website", style="green")
        table.add_column("Username", style="white")
        table.add_column("Password", style="magenta")
        table.add_column("PIN", style="yellow")

        sorted_keys = sorted(data.keys())
        for svc in sorted_keys:
            if query.lower() in svc.lower():
                info = data[svc]
                table.add_row(svc, info.get("website", "N/A"), info["username"], info["password"], info.get("pin", "N/A"))
        console.print(table)

    def check_expirations(self):
        """
        Displays all entries with masked data.
        """
        data = self.load_vault()
        if not data:
            console.print("[yellow]Vault is empty.[/yellow]")
            return

        table = Table(title="Vault Overview", border_style="green", show_lines=True, width=console.width)
        table.add_column("Service", style="cyan", no_wrap=True)
        table.add_column("Website", style="green")
        table.add_column("Username", style="white")
        table.add_column("Password", style="magenta")
        table.add_column("PIN", style="yellow")
        table.add_column("Status", style="bold yellow")

        today = datetime.now()
        sorted_keys = sorted(data.keys())
        for svc in sorted_keys:
            info = data[svc]
            last_date = datetime.strptime(info["last_updated"], "%Y-%m-%d")
            
            if (today - last_date).days > 90:
                status = "[blink red]EXPIRED[/blink red]"
            else:
                status = "Secure"
                
            table.add_row(svc, info.get("website", "N/A"), info["username"], "********", "****", status)
        console.print(table)

def main():
    console.print("[bold green]INITIALIZING CIPHER VAULT...[/bold green]", justify="center")
    master_key = Prompt.ask("[bold cyan]Enter Master Encryption Key[/bold cyan]", password=True)
    vault = CipherVault(master_key)
    
    if vault.load_vault() is None: 
        return

    vault.check_expirations()
    while True:
        console.print("\n[bold green]1.[/bold green] View All [bold green]2.[/bold green] Add [bold blue]3. Update[/bold blue] [bold green]4.[/bold green] Search [bold cyan]5. Rename[/bold cyan] [bold red]6. Delete[/bold red] [bold green]7.[/bold green] Exit")
        choice = Prompt.ask("Action", choices=["1", "2", "3", "4", "5", "6", "7"])
        
        if choice == "1":
            vault.check_expirations()
        elif choice == "2":
            vault.add_password()
        elif choice == "3":
            vault.update_entry()
        elif choice == "4":
            vault.search_entries()
        elif choice == "5":
            old = Prompt.ask("Rename Service (or 'exit')")
            if old.lower() != "exit":
                data = vault.load_vault()
                if data is not None and old in data:
                    new = Prompt.ask("New Name (or 'exit')")
                    if new.lower() != "exit":
                        data[new] = data.pop(old)
                        vault.save_vault(data)
                        console.print("[bold green][*][/bold green] Renamed.")
        elif choice == "6":
            svc = Prompt.ask("Delete Service (or 'exit')")
            if svc.lower() != "exit":
                data = vault.load_vault()
                if data is not None and svc in data:
                    if Prompt.ask("Confirm Delete?", choices=["y", "n"]) == "y":
                        del data[svc]
                        vault.save_vault(data)
                        console.print("[bold yellow][-][/bold yellow] Removed.")
        elif choice == "7":
            break

if __name__ == "__main__":
    main()