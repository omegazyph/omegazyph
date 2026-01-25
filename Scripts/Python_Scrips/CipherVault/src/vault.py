# Date: 2026-01-25
# Script Name: vault.py
# Author: omegazyph
# Updated: 2026-01-25
# Description: A Zero-Trust local password manager utilizing AES-256 encryption.
# Features: Rename service, explicit auto-generated passwords, automated backups, 
# A-Z sorting, and service deletion. Full non-shorthand version.

import os
import json
import base64
import secrets
import string
import shutil
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

# Initialize Rich console for the stylized hacker aesthetic
console = Console()

class CipherVault:
    def __init__(self, master_password):
        """
        Initializes pathing and creates necessary data/backup directories.
        Calculates absolute paths relative to the script location.
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)
        
        # Setup absolute paths for the data and backup folders
        self.data_dir = os.path.join(parent_dir, "data")
        self.backup_dir = os.path.join(self.data_dir, "backups")
        self.file_path = os.path.join(self.data_dir, "vault_data.bin")
        
        # Create directories if they do not exist
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

        # Derive the key and initialize the cipher
        self.key = self._derive_key(master_password)
        self.cipher = Fernet(self.key)
        self.expiration_days = 90

    def _derive_key(self, password):
        """
        Derives a cryptographic key from the master password using PBKDF2.
        Explicitly handles the KDF process.
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
        Creates a timestamped copy of the vault file in the backups folder.
        """
        if os.path.exists(self.file_path):
            current_time = datetime.now()
            timestamp = current_time.strftime("%Y%m%d_%H%M%S")
            backup_name = "backup_" + timestamp + ".bin"
            backup_path = os.path.join(self.backup_dir, backup_name)
            shutil.copy2(self.file_path, backup_path)
            console.print(f"[dim cyan]System: Auto-backup complete ({backup_name})[/dim cyan]")

    def load_vault(self):
        """
        Decrypts the binary file into a readable dictionary.
        """
        if not os.path.exists(self.file_path):
            return {}
        
        try:
            with open(self.file_path, "rb") as vault_file:
                encrypted_data = vault_file.read()
                decrypted_data = self.cipher.decrypt(encrypted_data)
                vault_json = decrypted_data.decode()
                return json.loads(vault_json)
        except Exception:
            console.print("[bold red]ERROR:[/bold red] Authentication failed.")
            return None

    def save_vault(self, data):
        """
        Encrypts the dictionary and writes to disk, then triggers a backup.
        """
        json_string = json.dumps(data)
        json_bytes = json_string.encode()
        encrypted_data = self.cipher.encrypt(json_bytes)
        
        with open(self.file_path, "wb") as vault_file:
            vault_file.write(encrypted_data)
        
        # Trigger explicit backup
        self._create_backup()

    def generate_password(self):
        """
        Generates a high-entropy random password using an explicit loop.
        """
        length = 18
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password_list = []
        
        for i in range(length):
            char = secrets.choice(alphabet)
            password_list.append(char)
            
        secure_password = "".join(password_list)
        return secure_password

    def rename_service(self, old_name):
        """
        Explicitly renames a service key while preserving its data.
        """
        data = self.load_vault()
        if data is not None:
            if old_name in data:
                new_name = Prompt.ask(f"Enter new name for [bold cyan]{old_name}[/bold cyan]")
                
                if new_name in data:
                    console.print("[red]Error: A service with that name already exists.[/red]")
                else:
                    # Move the data to the new key and delete the old one
                    service_info = data.pop(old_name)
                    data[new_name] = service_info
                    self.save_vault(data)
                    console.print(f"[bold green][*][/bold green] Service renamed to {new_name}.")
            else:
                console.print(f"[red]Service '{old_name}' not found in vault.[/red]")

    def delete_entry(self, service_name):
        """
        Removes a specific service and updates the vault and backups.
        """
        data = self.load_vault()
        if data is not None:
            if service_name in data:
                confirm = Prompt.ask(f"Delete [bold red]{service_name}[/bold red]?", choices=["y", "n"], default="n")
                if confirm == "y":
                    del data[service_name]
                    self.save_vault(data)
                    console.print(f"[bold yellow][-][/bold yellow] {service_name} removed.")
            else:
                console.print(f"[red]Service '{service_name}' not found.[/red]")

    def add_password(self, service, username, password):
        """
        Adds or updates a service entry with explicit date handling.
        """
        data = self.load_vault()
        if data is not None:
            current_date = datetime.now()
            date_string = current_date.strftime("%Y-%m-%d")
            
            new_entry = {
                "username": username,
                "password": password,
                "last_updated": date_string
            }
            
            data[service] = new_entry
            self.save_vault(data)
            console.print(f"[bold green][+][/bold green] Credentials for {service} secured.")

    def search_entries(self, query):
        """
        Search function with explicit A-Z sorting loop.
        """
        data = self.load_vault()
        if data is None:
            return
            
        search_table = Table(title=f"Search Results: {query}", border_style="blue")
        search_table.add_column("Service", style="cyan")
        search_table.add_column("Username", style="white")
        search_table.add_column("Password", style="magenta")

        service_keys = sorted(data.keys())
        for service in service_keys:
            if query.lower() in service.lower():
                info = data[service]
                search_table.add_row(service, info["username"], info["password"])
        
        console.print(search_table)

    def check_expirations(self):
        """
        Main view with A-Z sorting and status check loop.
        """
        data = self.load_vault()
        if not data:
            console.print("[yellow]The vault is currently empty.[/yellow]")
            return

        table = Table(title="[bold green]Vault Integrity Status[/bold green]", border_style="green")
        table.add_column("Service", style="cyan")
        table.add_column("Username", style="white")
        table.add_column("Status", style="bold yellow")

        today = datetime.now()
        service_keys = sorted(data.keys())
        
        for service in service_keys:
            info = data[service]
            last_updated_str = info["last_updated"]
            last_date = datetime.strptime(last_updated_str, "%Y-%m-%d")
            
            time_diff = today - last_date
            if time_diff > timedelta(days=self.expiration_days):
                status_label = "[blink red]EXPIRED[/blink red]"
            else:
                status_label = "Secure"
                
            table.add_row(service, info["username"], status_label)

        console.print(table)

def main():
    console.print("[bold green]INITIALIZING CIPHER VAULT...[/bold green]", justify="center")
    
    master_key = Prompt.ask("[bold cyan]Enter Master Encryption Key[/bold cyan]", password=True)
    vault = CipherVault(master_key)
    
    vault.check_expirations()

    while True:
        console.print("\n[bold green]1.[/bold green] View All")
        console.print("[bold green]2.[/bold green] Add Entry")
        console.print("[bold green]3.[/bold green] Search Service")
        console.print("[bold cyan]4. Rename Service[/bold cyan]")
        console.print("[bold red]5. Delete Entry[/bold red]")
        console.print("[bold green]6.[/bold green] Exit")
        
        choice = Prompt.ask("Action", choices=["1", "2", "3", "4", "5", "6"])

        if choice == "1":
            vault.check_expirations()
            
        elif choice == "2":
            svc = Prompt.ask("Service Name")
            user = Prompt.ask("Username")
            
            gen_option = Prompt.ask("Generate secure password?", choices=["y", "n"], default="y")
            if gen_option == "y":
                pwd = vault.generate_password()
                console.print(f"[bold yellow]Generated:[/bold yellow] {pwd}")
            else:
                pwd = Prompt.ask("Enter Password", password=True)
                
            vault.add_password(svc, user, pwd)
            
        elif choice == "3":
            keyword = Prompt.ask("Enter Service Keyword")
            vault.search_entries(keyword)
            
        elif choice == "4":
            svc_to_rename = Prompt.ask("Enter the service name you want to change")
            vault.rename_service(svc_to_rename)
            
        elif choice == "5":
            svc_to_del = Prompt.ask("Enter the EXACT Service Name to delete")
            vault.delete_entry(svc_to_del)
            
        elif choice == "6":
            console.print("[bold green]Closing secure session. Stay secure, Wayne.[/bold green]")
            break

if __name__ == "__main__":
    main()