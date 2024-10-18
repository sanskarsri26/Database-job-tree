import csv
import sqlite3

# Sample input Do not delete
csv_file_path = '/Users/sanskarsrivastava/Desktop/CSE/Database-job/Data/Processed_full_fluxes_Map_file_soil_QUI-02_2023-05-05.csv'

#csv_file_path = "/Users/sanskarsrivastava/Desktop/CSE/Database-job/Data/Processed_short_fluxes_Map_file_soil_QUI-02_2023-05-05.csv"
# Define the name of your SQLite database
sqlite_db_path = 'post_soil_flux.db'

# Connect to the SQLite database (or create it if it doesn't exist)
connection = sqlite3.connect(sqlite_db_path)
cursor = connection.cursor()

# Open the CSV file
with open(csv_file_path, newline='') as csvfile:
    # Use DictReader to read the CSV file, which uses the first row as column names
    csv_reader = csv.DictReader(csvfile)
    
    # Extract column names from the CSV file
    column_names = csv_reader.fieldnames
    
    # Handle duplicate columns for "plot_number" and "Date_time"
    seen_columns = set()
    unique_columns = []
    
    for column in column_names:
        column_lower = column.lower()  # For case-insensitive comparison
        
        # Handle duplicate "plot_number"
        if column_lower == "plot_number" and "plot_number" in seen_columns:
            continue  # Skip the second "plot_number"
        
        # Handle duplicate "Date_time"
        if column_lower == "date_time" and "date_time" in seen_columns:
            continue  # Skip the second "Date_time"
        
        unique_columns.append(column)
        seen_columns.add(column_lower)  # Ensure case-insensitive uniqueness
    
    # Log the unique columns for debugging
    print("Unique Columns:", unique_columns)
    
    # Create a table with columns based on the CSV headers
    create_table_query = f'''
    CREATE TABLE IF NOT EXISTS post_soil_flux (
        {', '.join([f"{column} TEXT" for column in unique_columns])}
    );
    '''
    
    # Execute the table creation command
    try:
        cursor.execute(create_table_query)
    except sqlite3.OperationalError as e:
        print("Error during table creation:", e)
        connection.close()
        raise e
    
    # Prepare SQL command for inserting data
    insert_query = f'INSERT INTO post_soil_flux ({", ".join(unique_columns)}) VALUES ({", ".join(["?" for _ in unique_columns])})'
    
    # Insert each row from the CSV file into the table
    for row in csv_reader:
        # Adjust row data to ensure it matches unique columns
        adjusted_row = {column: row[column] for column in unique_columns}
        # Log the adjusted row for debugging
        print("Inserting Row:", adjusted_row)
        cursor.execute(insert_query, [adjusted_row[column] for column in unique_columns])

# Commit changes and close the connection to the database
connection.commit()
connection.close()

print("CSV data imported successfully, and duplicate 'plot_number' and 'Date_time' removed!")
