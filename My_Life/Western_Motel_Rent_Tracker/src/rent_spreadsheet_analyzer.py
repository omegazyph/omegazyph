import os
import pandas

# Project Folder: Western_Motel_Rent_Tracker
# File Location: Western_Motel_Rent_Tracker/src/rent_spreadsheet_analyzer.py
# Date Created: May 19, 2026
# Date Updated: May 19, 2026
# Author: omegazyph
# Description: This program opens and analyzes OpenDocument Spreadsheet (.ods) files 
# tracking rent payments for the Western Motel. It uses absolute path resolution 
# based on the script location to find files reliably across different terminal environments.

def analyze_rent_spreadsheet(file_path, monthly_rate, total_months_elapsed):
    """
    Reads an OpenDocument Spreadsheet file, displays its structure, 
    and calculates the total rent paid and remaining balance.
    """
    print("=" * 60)
    print(f"Analyzing File: {os.path.basename(file_path)}")
    print("=" * 60)
    
    try:
        # Load the spreadsheet file using pandas with the OpenDocument format engine
        excel_file_reader = pandas.ExcelFile(file_path, engine="odf")
        sheet_names_list = excel_file_reader.sheet_names
        print(f"Found sheets: {sheet_names_list}")
        
        total_payments_across_all_sheets = 0.0
        
        for sheet_name in sheet_names_list:
            print(f"\nProcessing Sheet: {sheet_name}")
            # Read the specific sheet into a pandas DataFrame
            data_frame = pandas.read_excel(file_path, sheet_name=sheet_name, engine="odf")
            
            # Display the first few rows to help verify the data structure
            print("First few rows of data:")
            print(data_frame.head())
            
            # Display information about the columns found in the sheet
            print("\nColumn Names found:")
            for column_name in data_frame.columns:
                print(f" - {column_name}")
            
            # Attempt to automatically find a column related to payment amounts
            payment_column_name = None
            for column_name in data_frame.columns:
                lowercase_column_name = str(column_name).lower()
                if "paid" in lowercase_column_name or "amount" in lowercase_column_name or "payment" in lowercase_column_name:
                    payment_column_name = column_name
                    break
            
            if payment_column_name:
                print(f"\nAutomatically identified payment column: '{payment_column_name}'")
                # Convert the column to numeric values, treating errors safely as zero
                numeric_payments = pandas.to_numeric(data_frame[payment_column_name], errors="coerce").fillna(0.0)
                sheet_total_payments = float(numeric_payments.sum())
                print(f"Total payments calculated from this sheet: {sheet_total_payments} dollars")
                total_payments_across_all_sheets += sheet_total_payments
            else:
                print("\nCould not automatically identify a payment column.")
                print("Please review the column names listed above and update the script if necessary.")
        
        # Calculate final balances based on time elapsed
        total_rent_owed = monthly_rate * total_months_elapsed
        remaining_balance = total_rent_owed - total_payments_across_all_sheets
        
        print("\n" + "-" * 40)
        print("SPREADSHEET ANALYSIS SUMMARY")
        print("-" * 40)
        print(f"Monthly Rent Rate: {monthly_rate} dollars")
        print(f"Total Months Elapsed: {total_months_elapsed} months")
        print(f"Total Accumulated Rent Owed: {total_rent_owed} dollars")
        print(f"Total Payments Extracted: {total_payments_across_all_sheets} dollars")
        print(f"Current Remaining Balance: {remaining_balance} dollars")
        print("-" * 40)
        
    except Exception as exception_message:
        print(f"An error occurred while reading the file: {exception_message}")
        print("Please ensure that the 'odfpy' library is installed in your environment.")

def main():
    # Define parameters matching your rent structure
    monthly_rent_rate = 525
    total_months_elapsed = 13  # From May 2025 through May 2026 inclusive
    
    # Get the absolute directory path where this specific script file lives
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Navigate up one directory from 'src' to the project root, then into the 'data' folder
    data_directory = os.path.abspath(os.path.join(script_directory, "..", "data"))
    
    file_names_list = [
        "2025 Western Motel Rent Payments.ods",
        "2026 Western Motel Rent Payments.ods"
    ]
    
    # Process each spreadsheet file if it exists in the resolved data directory
    for file_name in file_names_list:
        full_file_path = os.path.join(data_directory, file_name)
        if os.path.exists(full_file_path):
            analyze_rent_spreadsheet(
                file_path=full_file_path,
                monthly_rate=monthly_rent_rate,
                total_months_elapsed=total_months_elapsed
            )
        else:
            print(f"\nFile not found: {full_file_path}")
            print(f"Please ensure your '{file_name}' file is placed inside the 'data' directory.")

if __name__ == "__main__":
    main()