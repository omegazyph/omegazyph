<?php
// =============================================================================
// Date:           2026-11-23
// Script Name:    php_starter.php
// Author:         Omegazyph
// Updated:        2026-11-23
// Description:    Starter PHP script providing ANSI terminal colors, formatted
//                 status and info output, and a centered banner helper.
// File Structure: project_root/
//                     php_starter.php
// =============================================================================

// region --- ANSI Color Codes ---
// Define ANSI escape sequences for terminal colors and formatting
define("BLUE", "\033[1;34m");
define("BOLD", "\033[1m");
define("CYAN", "\033[1;36m");
define("GREEN", "\033[1;32m");
define("MAGENTA", "\033[38;2;255;0;144m");
define("PURPLE", "\033[1;35m");
define("RED", "\033[1;31m");
define("RESET", "\033[0m");
define("YELLOW", "\033[1;33m");
// endregion

// region --- User Interface Functions ---
/**
 * Print a line of text in the specified ANSI color and reset formatting afterward.
 */
function print_color(string $text, string $color = CYAN): void
{
    // Apply the starting color escape sequence, print text, and reset formatting
    echo $color . $text . RESET . PHP_EOL;
}

/**
 * Print a dynamically centered banner with top and bottom borders.
 */
function print_ascii_banner(string $banner_title = "Default Title Starting"): void
{
    // Set the total character width for the banner border
    $total_width = 65;

    // Calculate leading spaces needed to center the title inside the banner
    $title_length = strlen($banner_title);
    $padding = intdiv(max(0, $total_width - $title_length), 2);

    // Build the leading space string and horizontal border line
    $leading_spaces = str_repeat(" ", $padding);
    $border_line = str_repeat("=", $total_width);

    // Print top border, centered title, and bottom border
    print_color(PURPLE . $border_line);
    print_color(BOLD . BLUE . $leading_spaces . $banner_title);
    print_color(PURPLE . $border_line);
}

/**
 * Print formatted messages with distinct prefixes and colors by message type.
 */
function print_message(string $message_type, string $message_text = ""): void
{
    // Match message_type to its corresponding tag and ANSI color
    if ($message_type === "error") {
        print_color(BOLD . RED . "[X] " . $message_text);
    } elseif ($message_type === "info") {
        // Use [*] in BLUE for general informational notes
        print_color(BOLD . BLUE . "[*] " . $message_text);
    } elseif ($message_type === "status") {
        // Use [~] in 24-bit MAGENTA for active status and progress updates
        print_color(BOLD . MAGENTA . "[~] " . $message_text);
    } elseif ($message_type === "success") {
        print_color(BOLD . GREEN . "[+] " . $message_text);
    } elseif ($message_type === "warning") {
        print_color(BOLD . YELLOW . "[!] " . $message_text);
    } else {
        // Print plain text when no recognized message category is provided
        echo $message_text . PHP_EOL;
    }
}
// endregion

// region --- Main Process ---
/**
 * Run the main demonstration workflow for the starter script.
 */
function main(): void
{
    // Clear the terminal screen across Windows and Unix-like systems
    if (stripos(PHP_OS, "WIN") === 0) {
        system("cls");
    } else {
        system("clear");
    }

    // Display the opening banner
    print_ascii_banner("Put your Title here");

    // Output sample messages across each supported message category
    print_message("status", "Initializing module checks");
    print_message("info", "This is an informational line");
    print_message("warning", "Please wait, this may take a few seconds");
    print_message("success", "Initialization complete!");
    print_message("error", "Sample error message.");

    // Display the closing banner
    print_ascii_banner("Put your ending title here");
}
// endregion

// Execute main only when this file is run directly as the entry script
if (isset($_SERVER["SCRIPT_FILENAME"]) && realpath($_SERVER["SCRIPT_FILENAME"]) === __FILE__) {
    main();
}
?>