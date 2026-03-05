#!/bin/zsh -e

# Script Header
# Author: Wayne Stock
# Date: 2024-08-14
# Description: This script performs system maintenance tasks including updating the package manager,
# upgrading packages, removing obsolete files, and verifying the Bash version. It uses `apt-get` for
# package management and includes pauses between commands for better readability.

# Update package manager
echo "Updating package manager..."
sudo apt-get update
echo ""  # Print a blank line for readability
sleep 2  # Pause for 2 seconds

# Upgrade all packages, including Bash
echo "Upgrading all packages, including Bash..."
sudo apt-get dist-upgrade -y
echo ""  # Print a blank line for readability
sleep 2  # Pause for 2 seconds

# Remove obsolete packages and their configuration files
echo "Removing any obsolete packages and their configuration files..."
sudo apt-get autoremove --purge -y
echo ""  # Print a blank line for readability
sleep 2  # Pause for 2 seconds

# Remove downloaded package files that are no longer needed
echo "Removing any downloaded package files that are no longer needed..."
sudo apt-get autoclean -y
echo ""  # Print a blank line for readability
sleep 2  # Pause for 2 seconds

# Remove old kernels and their configuration files (Note: This is redundant with the previous autoremove command)
echo "Removing old kernels and their configuration files..."
sudo apt-get autoremove --purge -y
echo ""  # Print a blank line for readability
sleep 2  # Pause for 2 seconds

# Verify the Bash version
echo "Verifying Bash version..."
zsh -c 'bash --version'
echo ""  # Print a blank line for readability
sleep 2  # Pause for 2 seconds

# Clean up any package files that are no longer needed
echo "Cleaning up any package files that are no longer needed..."
sudo apt-get clean -y
echo ""  # Print a blank line for readability
sleep 2  # Pause for 2 seconds

# Completion message
echo "Done."
