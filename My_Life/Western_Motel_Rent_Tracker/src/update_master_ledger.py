import csv
import json
import os

# Project Folder: Master_Expense_Tracker
# File Location: Master_Expense_Tracker/src/update_master_ledger.py
# Date Created: May 19, 2026
# Date Updated: May 19, 2026
# Author: omegazyph
# Description: This program processes historical rent information into a master 
# database ledger. It strictly relies on an external 'settings.json' file for 
# establishing paths, tracking file names, header strings, and execution rules, 
# ensuring that no environmental variables or fallback values are hardcoded.

def load_external_settings(settings_file_path):
    """
    Reads the global JSON configuration parameters from disk. Halts execution 
    immediately if the configuration workspace is missing or unreadable.
    """
    if not os.path.exists(settings_file_path):
        print("--------------------------------------------------------")
        print("CRITICAL ERROR: Configuration settings file not found at:")
        print(f" -> {settings_file_path}")
        print("--------------------------------------------------------")
        raise FileNotFoundError(f"Missing required configuration: {settings_file_path}")
        
    with open(settings_file_path, "r") as opened_settings_file:
        return json.load(opened_settings_file)

def read_master_json_database(json_file_path):
    """
    Loads your existing personal profile database file. Halts immediately 
    if the master expense profile is missing.
    """
    if not os.path.exists(json_file_path):
        print("--------------------------------------------------------")
        print("CRITICAL ERROR: Master data registry not found at:")
        print(f" -> {json_file_path}")
        print("--------------------------------------------------------")
        raise FileNotFoundError(f"Missing master expense registry: {json_file_path}")
        
    with open(json_file_path, "r") as opened_json_file:
        return json.load(opened_json_file)

def import_csv_rows_via_settings(csv_file_path, parsing_rules_dictionary):
    """
    Parses compiled transaction elements rows matching string constraints 
    provided inside our dynamic configurations layout.
    """
    compiled_records_list = []
    
    if not os.path.exists(csv_file_path):
        print("--------------------------------------------------------")
        print("CRITICAL ERROR: Tabular export tracking file not found at:")
        print(f" -> {csv_file_path}")
        print("--------------------------------------------------------")
        raise FileNotFoundError(f"Missing data table track: {csv_file_path}")

    # Pull structural columns tracking values out of settings maps
    column_labels = parsing_rules_dictionary.get("expected_columns", [])
    
    with open(csv_file_path, "r", newline="") as opened_csv_file:
        csv_table_reader = csv.DictReader(opened_csv_file)
        
        for individual_row_data in csv_table_reader:
            # Clean and isolate numerical floats out of raw currency string items
            clean_paid = individual_row_data[column_labels[1]].replace("$", "").replace(",", "").strip()
            clean_owed = individual_row_data[column_labels[2]].replace("$", "").replace(",", "").replace("-", "").strip()
            clean_balance = individual_row_data[column_labels[3]].replace("$", "").replace(",", "").strip()
            
            structured_record = {
                "due_date": individual_row_data[column_labels[0]].strip(),
                "amount_paid_dollars": float(clean_paid) if clean_paid else 0.0,
                "amount_owed_dollars": float(clean_owed) if clean_owed else 0.0,
                "remaining_balance_dollars": float(clean_balance) if clean_balance else 0.0,
                "date_paid": individual_row_data[column_labels[4]].strip(),
                "notes": individual_row_data[column_labels[5]].strip()
            }
            compiled_records_list.append(structured_record)
            
    return compiled_records_list

def main():
    # Pinpoint local script file directory context targets
    script_directory_path = os.path.dirname(os.path.abspath(__file__))
    data_directory_path = os.path.abspath(os.path.join(script_directory_path, "..", "data"))
    
    # Establish full absolute workspace reference coordinates for setting keys
    settings_file_path = os.path.join(data_directory_path, "settings.json")
    
    # Load settings profiles from drive properties
    print("Loading environmental execution settings profiles...")
    configuration_profile = load_external_settings(settings_file_path=settings_file_path)
    
    # Extract path keys and rules dictionaries from configurations maps
    path_rules = configuration_profile.get("project_paths", {})
    parsing_rules = configuration_profile.get("spreadsheet_parsing_rules", {})
    ingestion_rules = configuration_profile.get("ingestion_flags", {})
    
    # Resolve target file locations derived completely from the settings layout
    master_json_file_path = os.path.join(data_directory_path, path_rules.get("master_ledger_filename"))
    source_csv_file_path = os.path.join(data_directory_path, path_rules.get("compiled_csv_filename"))
    
    # Process core dataset files
    print("Reading master database ledger structures...")
    master_ledger_dictionary = read_master_json_database(json_file_path=master_json_file_path)
    
    print("Importing table elements out of reference CSV file records...")
    fresh_rent_history_records = import_csv_rows_via_settings(
        csv_file_path=source_csv_file_path, 
        parsing_rules_dictionary=parsing_rules
    )
    
    # Append the historical log array into the target key set by our configurations
    target_key = ingestion_rules.get("target_json_destination_key", "rent_payment_history_ledger")
    master_ledger_dictionary[target_key] = fresh_rent_history_records
    
    # Perform operational total calculations if checked true inside configuration flags
    if ingestion_rules.get("calculate_financial_summary", True):
        total_rent_paid_to_date = sum(item["amount_paid_dollars"] for item in fresh_rent_history_records)
        total_rent_outstanding_balance = sum(item["remaining_balance_dollars"] for item in fresh_rent_history_records)
        
        master_ledger_dictionary["financial_summary_metadata"] = {
            "total_rent_paid_all_time_dollars": round(total_rent_paid_to_date, 2),
            "total_rent_balance_remaining_dollars": round(total_rent_outstanding_balance, 2)
        }
    
    # Write the completed database file modification array out to disk storage
    print(f"Saving merged layout records to file: {master_json_file_path}")
    with open(master_json_file_path, "w") as destination_json_file:
        json.dump(master_ledger_dictionary, destination_json_file, indent=4)
        
    print("\n========================================================")
    print("    SETTINGS-DRIVEN MASTER CONFIGURATION PIPELINE       ")
    print("========================================================")
    print(f" -> Database Ingestion Point: [{target_key}]")
    print(f" -> Records Synced Successfully: {len(fresh_rent_history_records)} elements")
    if ingestion_rules.get("calculate_financial_summary", True):
        print(f" -> Total Rent Paid In History:  ${total_rent_paid_to_date:,.2f}")
        print(f" -> Outstanding Balance Total:   ${total_rent_outstanding_balance:,.2f}")
    print("========================================================\n")

if __name__ == "__main__":
    main()