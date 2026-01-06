'''
This file can run under all 3 version of python
'''


import subprocess

# Function to run shell commands
def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return str(e)

# Check for updates
print("Checking for updates...")
update_info = run_command("sudo apt-get update -y")
print(update_info)

# Upgrade all packages
print("\nUpgrading all packages, including Bash...")
upgrade_info = run_command("sudo apt-get dist-upgrade -y")
print(upgrade_info)

#Update Exploit Database
print("\nInstall and update Exploit Database")
exploit_info = run_command("sudo apt-get install exploitdb -y")
print(exploit_info)


#Update Searchsploit
print("\nUpgrading Searchsploit....")
searchploit_info = run_command("sudo apt-get searchsploit -u")
print(searchploit_info)

#Update Nmap
print("\nUpdateing nmap....")
nmap_info = run_command("sudo nmap --script-updatedb")
print(nmap_info)

########################################################
# Cleaning

# Autoremove unused packages
print("\nRemoving any obsolete packages and their configuration files...")
autoremove_info = run_command("sudo apt-get autoremove --purge -y")
print(autoremove_info)

#Autoclean
print("\nRemoving any downloaded files that are no longer needed...")
autoclean_info = run_command("sudo apt-get autoclean -y")
print(autoclean_info)

# Verify Bash Veraion
print("\nVerify Bash Version...")
bash_version_info = run_command("bash --version")
print(bash_version_info)
