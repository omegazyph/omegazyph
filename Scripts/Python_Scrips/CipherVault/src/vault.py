# Date: 2026-01-25
# Script Name: vault.py
# Author: omegazyph
# Updated: 2026-01-25
# Description: A Zero-Trust local password manager utilizing AES-256 encryption.
# Features: Security Countdown Timer, Universal 'exit' support, Dynamic grid UI, 
# Explicit logic for Ruff compatibility, and automated binary backups.
# Fixes: Removed unused local variable assignments for 'data'.

import os
import json
import base64
import secrets
import string
import shutil
import time
from datetime import datetime

# Cryptography imports
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

# Rich UI imports
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.live import Live

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
        
        # Explicit folder structure
        self.data_dir = os.path.join(parent_dir, "data")
        self.backup_dir = os.path.join(self.data_dir, "backups")
        self.file_path = os.path.join(self.data_dir, "vault_data.bin")
        
        # Check and create directories using 'not' checks
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

    def _display_secure_timer(self, label, value, seconds=10):
        """
        Displays sensitive data with a countdown, then wipes the line for security.
        """
        with Live(console=console, screen=False, refresh_per_second=1) as live:
            current_second = seconds
            while current_second > 0:
                display_text = "[bold yellow]" + label + ":[/bold yellow] [bold white]" + value + "[/bold white] [dim](Clearing in " + str(current_second) + "s...)[/dim]"
                live.update(display_text)
                time.sleep(1)
                current_second = current_second - 1
                
        console.print("[bold red]" + label + " CLEARED FROM SCREEN[/bold red] " + (" " * 20))

    def load_vault(self):
        """
        Decrypts the vault file and returns data as a dictionary.
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
            console.print("[bold red]ERROR:[/bold red] Authentication failed or corrupted file.")
            return None

    def save_vault(self, data):
        """
        Encrypts and saves data dictionary with an automated backup.
        """
        json_string = json.dumps(data)
        json_bytes = json_string.encode()
        encrypted_data = self.cipher.encrypt(json_bytes)
        with open(self.file_path, "wb") as vault_file:
            vault_file.write(encrypted_data)
        
        if os.path.exists(self.file_path):
            current_time = datetime.now()
            timestamp = current_time.strftime("%Y%m%d_%H%M%S")
            backup_name = "backup_" + timestamp + ".bin"
            backup_path = os.path.join(self.backup_dir, backup_name)
            shutil.copy2(self.file_path, backup_path)

    def generate_password(self):
        """
        Generates an 18-character secure random password.
        """
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password_list = []
        for i in range(18):
            random_char = secrets.choice(alphabet)
            password_list.append(random_char)
        secure_password = "".join(password_list)
        return secure_password

    def update_entry(self):
        """
        Updates specific fields with 'exit' checks at every prompt.
        """
        service_name = Prompt.ask("Service to Update (or 'exit')")
        if service_name.lower() == "exit":
            return

        data = self.load_vault()
        if data is not None:
            if service_name in data:
                console.print("\n1. Website  2. Username  3. Password  4. PIN  5. Cancel")
                choice = Prompt.ask("Select field", choices=["1", "2", "3", "4", "5"])
                
                if choice == "5":
                    return

                new_val = Prompt.ask("Enter new value (or 'exit')")
                if new_val.lower() == "exit":
                    return

                if choice == "1":
                    data[service_name]["website"] = new_val
                elif choice == "2":
                    data[service_name]["username"] = new_val
                elif choice == "3":
                    data[service_name]["password"] = new_val
                elif choice == "4":
                    data[service_name]["pin"] = new_val

                data[service_name]["last_updated"] = datetime.now().strftime("%Y-%m-%d")
                self.save_vault(data)
                console.print("[bold green]Update successful for " + service_name + ".[/bold green]")
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
            self._display_secure_timer("GENERATED PASSWORD", pwd)
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
            console.print("[bold green][+][/bold green] Credentials for " + service + " secured.")

    def search_entries(self):
        """
        Search and display results using the security timer.
        """
        query = Prompt.ask("Keyword (or 'exit')")
        if query.lower() == "exit":
            return

        data = self.load_vault()
        if not data:
            return
            
        found_match = False
        sorted_keys = sorted(data.keys())
        for svc in sorted_keys:
            if query.lower() in svc.lower():
                found_match = True
                info = data[svc]
                console.print("\n[bold cyan]Entry: " + svc + "[/bold cyan]")
                console.print("Website: " + info.get("website", "N/A"))
                console.print("Username: " + info["username"])
                
                self._display_secure_timer("Password", info["password"])
                
                if info.get("pin", "N/A") != "N/A":
                    self._display_secure_timer("PIN", info["pin"])
        
        if not found_match:
            console.print("[yellow]No matches found for: " + query + "[/yellow]")

    def check_expirations(self):
        """
        Overview grid with masked data for privacy.
        """
        data = self.load_vault()
        if not data:
            console.print("[yellow]Vault is empty.[/yellow]")
            return
            
        table = Table(title="Vault Overview", border_style="green", show_lines=True, width=console.width)
        table.add_column("Service", style="cyan")
        table.add_column("Username", style="white")
        table.add_column("Status", style="bold yellow")

        today = datetime.now()
        sorted_keys = sorted(data.keys())
        for svc in sorted_keys:
            last_date_str = data[svc]["last_updated"]
            last_date = datetime.strptime(last_date_str, "%Y-%m-%d")
            
            days_passed = (today - last_date).days
            if days_passed > 90:
                status = "[blink red]EXPIRED[/blink red]"
            else:
                status = "Secure"
                
            table.add_row(svc, data[svc]["username"], status)
        console.print(table)

def main():
    """
    Main entry point for CipherVault.
    """
    console.print("[bold green]CIPHER VAULT INITIALIZING...[/bold green]", justify="center")
    master_key = Prompt.ask("Enter Master Key", password=True)
    vault = CipherVault(master_key)
    
    # Authenticate without leaving an unused 'data' variable
    if vault.load_vault() is None:
        return

    while True:
        console.print("\n1. View All  2. Add Entry  3. Update Field  4. Search  5. Exit")
        choice = Prompt.ask("Action", choices=["1", "2", "3", "4", "5"])
        
        if choice == "1":
            vault.check_expirations()
        elif choice == "2":
            vault.add_password()
        elif choice == "3":
            vault.update_entry()
        elif choice == "4":
            vault.search_entries()
        elif choice == "5":
            console.print("[bold green]Stay secure, Wayne.[/bold green]")
            break

if __name__ == "__main__":
    main()