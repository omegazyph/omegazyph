# Date: 2026-01-25
# Script Name: vault.py
# Author: omegazyph
# Updated: 2026-01-25
# Description: A Zero-Trust local password manager utilizing AES-256 encryption.
# Features: Dynamic window auto-sizing, Separated Grid UI, Website tracking, 
# PIN storage, Rename service, automated backups, and A-Z sorting.
# Fixes: Displays generated password immediately to the user.

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

# Initialize Rich console - tracks window size dynamically
console = Console()

class CipherVault:
    def __init__(self, master_password):
        """
        Initializes pathing and creates necessary data/backup directories.
        """
        script_path = os.path.abspath(__file__)
        script_dir = os.path.dirname(script_path)
        parent_dir = os.path.dirname(script_dir)
        
        # Folder structure logic as requested
        self.data_dir = os.path.join(parent_dir, "data")
        self.backup_dir = os.path.join(self.data_dir, "backups")
        self.file_path = os.path.join(self.data_dir, "vault_data.bin")
        
        # Creating folders if they do not exist
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
            console.print("[bold red]ERROR:[/bold red] Authentication failed or file corrupted.")
            return None

    def save_vault(self, data):
        """
        Encrypts and saves the data dictionary to the binary file.
        """
        json_string = json.dumps(data)
        json_bytes = json_string.encode()
        encrypted_data = self.cipher.encrypt(json_bytes)
        with open(self.file_path, "wb") as vault_file:
            vault_file.write(encrypted_data)
        self._create_backup()

    def generate_password(self):
        """
        Generates an 18-character secure random password using an explicit loop.
        """
        length = 18
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password_chars = []
        for i in range(length):
            char = secrets.choice(alphabet)
            password_chars.append(char)
        secure_password = "".join(password_chars)
        return secure_password

    def rename_service(self, old_name):
        """
        Safely renames a service key within the vault.
        """
        data = self.load_vault()
        if data is not None:
            if old_name in data:
                new_name = Prompt.ask("Enter new name for [bold cyan]" + old_name + "[bold cyan]")
                if new_name not in data:
                    data[new_name] = data.pop(old_name)
                    self.save_vault(data)
                    console.print("[bold green][*][/bold green] Service renamed to " + new_name + ".")
                else:
                    console.print("[red]Error: Name already exists.[/red]")

    def delete_entry(self, service_name):
        """
        Removes an entry from the vault after confirmation.
        """
        data = self.load_vault()
        if data is not None:
            if service_name in data:
                confirm = Prompt.ask("Delete [bold red]" + service_name + "[/bold red]?", choices=["y", "n"])
                if confirm == "y":
                    del data[service_name]
                    self.save_vault(data)
                    console.print("[bold yellow][-][/bold yellow] " + service_name + " removed.")

    def add_password(self, service, username, password, website, pin):
        """
        Adds a new credential entry to the vault.
        """
        data = self.load_vault()
        if data is not None:
            current_time = datetime.now()
            date_string = current_time.strftime("%Y-%m-%d")
            data[service] = {
                "username": username,
                "password": password,
                "website": website,
                "pin": pin,
                "last_updated": date_string
            }
            self.save_vault(data)
            console.print("[bold green][+][/bold green] Credentials for " + service + " secured.")

    def search_entries(self, query):
        """
        Searches the vault and displays unmasked results in a dynamic table.
        """
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
                table.add_row(
                    svc, 
                    info.get("website", "N/A"), 
                    info["username"], 
                    info["password"], 
                    info.get("pin", "N/A")
                )
        console.print(table)

    def check_expirations(self):
        """
        Displays all entries with masked passwords/PINs in a dynamic table.
        """
        data = self.load_vault()
        if not data:
            console.print("[yellow]Vault is empty.[/yellow]")
            return

        table = Table(title="Vault Overview (Privacy Mode)", border_style="green", show_lines=True, width=console.width)
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
            last_date_str = info["last_updated"]
            last_date = datetime.strptime(last_date_str, "%Y-%m-%d")
            
            diff = today - last_date
            if diff.days > self.expiration_days:
                status = "[blink red]EXPIRED[/blink red]"
            else:
                status = "Secure"
                
            table.add_row(
                svc, 
                info.get("website", "N/A"), 
                info["username"], 
                "********", 
                "****", 
                status
            )
        console.print(table)

def main():
    """
    Main entry point for the CipherVault application.
    """
    console.print("[bold green]INITIALIZING CIPHER VAULT...[/bold green]", justify="center")
    master_key = Prompt.ask("[bold cyan]Enter Master Encryption Key[/bold cyan]", password=True)
    vault = CipherVault(master_key)
    
    initial_data = vault.load_vault()
    if initial_data is None: 
        return

    vault.check_expirations()
    while True:
        console.print("\n[bold green]1.[/bold green] View All [bold green]2.[/bold green] Add [bold green]3.[/bold green] Search [bold cyan]4. Rename[/bold cyan] [bold red]5. Delete[/bold red] [bold green]6.[/bold green] Exit")
        choice = Prompt.ask("Action", choices=["1", "2", "3", "4", "5", "6"])
        
        if choice == "1": 
            vault.check_expirations()
        elif choice == "2":
            svc = Prompt.ask("Service")
            site = Prompt.ask("Website", default="N/A")
            user = Prompt.ask("Username")
            pin = Prompt.ask("PIN", default="N/A")
            
            gen_confirm = Prompt.ask("Generate password?", choices=["y", "n"], default="y")
            if gen_confirm == "y":
                pwd = vault.generate_password()
                # Explicitly showing the generated password before saving
                console.print("\n[bold yellow]SYSTEM GENERATED PASSWORD:[/bold yellow] [bold white]" + pwd + "[/bold white]\n")
            else:
                pwd = Prompt.ask("Password", password=True)
                
            vault.add_password(svc, user, pwd, site, pin)
        elif choice == "3": 
            keyword = Prompt.ask("Keyword")
            vault.search_entries(keyword)
        elif choice == "4": 
            rename_target = Prompt.ask("Service to Rename")
            vault.rename_service(rename_target)
        elif choice == "5": 
            delete_target = Prompt.ask("Service to Delete")
            vault.delete_entry(delete_target)
        elif choice == "6": 
            console.print("[bold green]Closing secure session. Stay secure, Wayne.[/bold green]")
            break

if __name__ == "__main__":
    main()