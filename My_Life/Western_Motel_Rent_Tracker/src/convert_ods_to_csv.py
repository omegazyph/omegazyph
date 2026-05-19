import csv
import glob
import os
import xml.etree.ElementTree as ElementTree
import zipfile

# Project Folder: Western_Motel_Rent_Tracker
# File Location: Western_Motel_Rent_Tracker/src/convert_ods_to_csv.py
# Date Created: May 19, 2026
# Date Updated: May 19, 2026
# Author: omegazyph
# Description: This program dynamically scans the 'data' directory for any 
# OpenDocument Spreadsheet (.ods) files. It automatically handles adding or 
# removing files from the folder, parses their internal XML structures, and 
# compiles them into a single, comprehensive CSV tracking sheet.

def extract_rows_from_open_document_sheet(file_path):
    """
    Unzips an OpenDocument spreadsheet file container and parses the core 
    XML text content to pull out raw row and column strings.
    """
    rows_extracted_list = []
    
    with zipfile.ZipFile(file_path, "r") as zip_archive_file:
        xml_content_bytes = zip_archive_file.read("content.xml")
        xml_element_root = ElementTree.fromstring(xml_content_bytes)
        
        open_document_namespaces = {
            "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
            "table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
            "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0"
        }
        
        tables_list = xml_element_root.findall(".//table:table", open_document_namespaces)
        for individual_table in tables_list:
            table_name = individual_table.get("{urn:oasis:names:tc:opendocument:xmlns:table:1.0}name")
            
            if table_name != "Sheet1":
                continue
                
            table_rows_list = individual_table.findall(".//table:table-row", open_document_namespaces)
            for individual_row in table_rows_list:
                cells_list = individual_row.findall(".//table:table-cell", open_document_namespaces)
                row_values_list = []
                
                for individual_cell in cells_list:
                    text_paragraphs_list = individual_cell.findall(".//text:p", open_document_namespaces)
                    cell_text_content = "".join([paragraph.text for paragraph in text_paragraphs_list if paragraph.text is not None])
                    
                    column_repeated_attribute = individual_cell.get("{urn:oasis:names:tc:opendocument:xmlns:table:1.0}number-columns-repeated")
                    if column_repeated_attribute:
                        repetition_threshold_count = min(int(column_repeated_attribute), 5)
                        row_values_list.extend([cell_text_content] * repetition_threshold_count)
                    else:
                        row_values_list.append(cell_text_content)
                
                if any(row_values_list):
                    rows_extracted_list.append(row_values_list)
                    
    return rows_extracted_list

def parse_rows_into_clean_records(raw_rows_list):
    """
    Filters out extraneous title rows, column labels, and formula total rows 
    to extract uniform data records for our transaction logging.
    """
    clean_records_list = []
    
    for row_elements in raw_rows_list:
        if not row_elements or len(row_elements) < 4:
            continue
            
        due_date_string = str(row_elements[0]).strip()
        
        if "Western" in due_date_string or "Date" in due_date_string or due_date_string == "":
            continue
            
        amount_paid_string = str(row_elements[1]).strip()
        amount_owed_string = str(row_elements[2]).strip()
        remaining_balance_string = str(row_elements[3]).strip()
        date_paid_string = str(row_elements[4]).strip() if len(row_elements) > 4 else ""
        notes_string = str(row_elements[5]).strip() if len(row_elements) > 5 else ""
        
        clean_records_list.append([
            due_date_string,
            amount_paid_string,
            amount_owed_string,
            remaining_balance_string,
            date_paid_string,
            notes_string
        ])
        
    return clean_records_list

def main():
    # Resolve local absolute folder paths matching the active script workspace
    script_directory = os.path.dirname(os.path.abspath(__file__))
    data_directory = os.path.abspath(os.path.join(script_directory, "..", "data"))
    
    # DYNAMIC SEARCH: Find all files ending in .ods inside the data folder automatically
    search_pattern = os.path.join(data_directory, "*.ods")
    found_spreadsheets = glob.glob(search_pattern)
    
    # Sort files alphabetically so the timelines stay chronological
    found_spreadsheets.sort()
    
    if not found_spreadsheets:
        print(f"No spreadsheet files (.ods) located inside the folder: {data_directory}")
        return
        
    master_rent_records_list = []
    
    print(f"Found {len(found_spreadsheets)} spreadsheet file(s) to process.")
    for full_ods_path in found_spreadsheets:
        filename_only = os.path.basename(full_ods_path)
        print(f" -> Processing rows from file: {filename_only}")
        
        raw_extracted_rows = extract_rows_from_open_document_sheet(file_path=full_ods_path)
        processed_rent_records = parse_rows_into_clean_records(raw_rows_list=raw_extracted_rows)
        master_rent_records_list.extend(processed_rent_records)
            
    # Set the destination path for the combined plain-text CSV export
    output_csv_file_path = os.path.join(data_directory, "combined_rent_payments.csv")
    
    print(f"Writing all combined entries out to: {output_csv_file_path}")
    with open(output_csv_file_path, "w", newline="") as destination_file:
        csv_data_writer = csv.writer(destination_file)
        
        # Write clean descriptive column headers
        csv_data_writer.writerow([
            "Due Date", 
            "Amount Paid", 
            "Amount Owed", 
            "Remaining Balance", 
            "Date Paid", 
            "Notes"
        ])
        
        # Write the compiled matrix of data entries
        csv_data_writer.writerows(master_rent_records_list)
        
    print(f"CSV compilation complete. Total database contains {len(master_rent_records_list)} monthly records.")

if __name__ == "__main__":
    main()