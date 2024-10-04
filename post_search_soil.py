import sqlite3

# Function to search rows based on 'plot_code'
def search_parcela_site(conn, Parcela_Site):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM post_soil_flux WHERE plot_code = ?", (Parcela_Site,))
    results = cursor.fetchall()
    cursor.close()
    return results

# Function to search rows based on 'Site'
def search_site(conn, Site):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM post_soil_flux WHERE Site = ?", (Site,))
    results = cursor.fetchall()
    cursor.close()
    return results

# Function to search rows based on a specific month
def search_by_month(conn, month):
    cursor = conn.cursor()
    query = "SELECT * FROM post_soil_flux WHERE strftime('%m', smpl_date) = ?"
    cursor.execute(query, (month,))
    results = cursor.fetchall()
    cursor.close()
    return results

# Function to search rows based on a specific year
def search_by_year(conn, year):
    cursor = conn.cursor()
    query = "SELECT * FROM post_soil_flux WHERE strftime('%Y', smpl_date) = ?"
    cursor.execute(query, (year,))
    results = cursor.fetchall()
    cursor.close()
    return results

# Function to search rows based on both month and year
def search_by_month_and_year(conn, month, year):
    cursor = conn.cursor()
    query = "SELECT * FROM post_soil_flux WHERE strftime('%m', smpl_date) = ? AND strftime('%Y', smpl_date) = ?"
    cursor.execute(query, (month, year))
    results = cursor.fetchall()
    cursor.close()
    return results

# Ensure the month is in 'MM' format
def format_month(month):
    return month.zfill(2) if len(month) == 1 else month

# Ensure the year is in 'YYYY' format
def format_year(year):
    return year.zfill(4) if len(year) < 4 else year

# Function to search rows based on 'sub_plot'
def search_mini_plot(conn, Miniplot):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM post_soil_flux WHERE sub_plot = ?", (Miniplot,))
    results = cursor.fetchall()
    cursor.close()
    return results

# Function to ensure the MiniPlot value is correctly formatted
def format_mini_plot(Miniplot):
    return Miniplot.strip()  # Remove any leading/trailing spaces

# Function to find duplicates based on plot_code, sub_plot, and CH4_finalflux_mgC_per_hr_m2
def find_duplicates(conn):
    cursor = conn.cursor()
    query = '''
        SELECT plot_code, sub_plot, CH4_finalflux_mgC_per_hr_m2, COUNT(*) as count
        FROM post_soil_flux
        GROUP BY plot_code, sub_plot, CH4_finalflux_mgC_per_hr_m2
        HAVING COUNT(*) > 1
    '''
    cursor.execute(query)
    duplicates = cursor.fetchall()
    cursor.close()
    return duplicates

# Function to list all rows that match a specific plot_code, sub_plot, and CH4_finalflux_mgC_per_hr_m2
def list_duplicate_rows(conn, plot_code, sub_plot, CH4_finalflux_mgC_per_hr_m2):
    cursor = conn.cursor()
    query = '''
        SELECT rowid, * FROM post_soil_flux
        WHERE plot_code = ? AND sub_plot = ? AND CH4_finalflux_mgC_per_hr_m2 = ?
    '''
    cursor.execute(query, (plot_code, sub_plot, CH4_finalflux_mgC_per_hr_m2))
    rows = cursor.fetchall()
    cursor.close()
    return rows

# Function to delete a specific row by rowid
def delete_row(conn, rowid):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM post_soil_flux WHERE rowid = ?", (rowid,))
    conn.commit()
    cursor.close()

# Function to handle duplicates and deletion of rows
def handle_duplicates(conn):
    duplicates = find_duplicates(conn)
    
    if not duplicates:
        print("No duplicate rows found.")
        return
    
    print("Duplicate rows found:")
    
    for dup in duplicates:
        plot_code, sub_plot, CH4_finalflux_mgC_per_hr_m2, count = dup
        print(f"\nDuplicate set: plot_code={plot_code}, sub_plot={sub_plot}, CH4_finalflux_mgC_per_hr_m2={CH4_finalflux_mgC_per_hr_m2}")
        rows = list_duplicate_rows(conn, plot_code, sub_plot, CH4_finalflux_mgC_per_hr_m2)
        
        for i, row in enumerate(rows):
            print(f"Row {i+1}: {row}")
        
        delete_choice = input("Do you want to delete one of these rows? (yes/no): ").lower()
        
        if delete_choice == 'yes':
            row_to_delete = int(input(f"Which row would you like to delete? Enter the row number (1-{len(rows)}): "))
            if 1 <= row_to_delete <= len(rows):
                rowid = rows[row_to_delete - 1][0]  # Get the rowid of the chosen row
                delete_row(conn, rowid)
                print(f"Row {row_to_delete} deleted.")
            else:
                print("Invalid row number. No rows deleted.")
        else:
            print("No rows deleted.")

# Main menu function to interact with the user
def main_menu():
    conn = sqlite3.connect("/Users/sanskarsrivastava/Desktop/CSE/Database-job/post_soil_flux.db")
    
    while True:
        print("\nMenu:")
        print("1. Search by Parcela_Site")
        print("2. Search by Site")
        print("3. Search by Month")
        print("4. Search by Year")
        print("5. Search by Month and Year")
        print("6. Search by Mini-Plot")
        print("7. Check for Duplicates")
        print("8. Exit")

        choice = input("Select an option (1-8): ")

        if choice == '1':
            parcela_site_to_search = input("Enter the Parcela_Site to search: ")
            results = search_parcela_site(conn, parcela_site_to_search)
            if results:
                print("Search Results:")
                for row in results:
                    print(row)
            else:
                print("No results found for the given Parcela_Site.")

        elif choice == '2':
            site_to_search = input("Enter the Site to search: ")
            results = search_site(conn, site_to_search)
            if results:
                print("Search Results:")
                for row in results:
                    print(row)
            else:
                print("No results found for the given Site.")

        elif choice == '3':
            month_input = input("Enter the month (MM) to search: ")
            month_input = format_month(month_input)  # Format the month
            results = search_by_month(conn, month_input)
            if results:
                print("Search Results:")
                for row in results:
                    print(row)
            else:
                print("No results found for the given month.")

        elif choice == '4':
            year_input = input("Enter the year (YYYY) to search: ")
            year_input = format_year(year_input)  # Format the year
            results = search_by_year(conn, year_input)
            if results:
                print("Search Results:")
                for row in results:
                    print(row)
            else:
                print("No results found for the given year.")

        elif choice == '5':
            month_input = input("Enter the month (MM) to search: ")
            month_input = format_month(month_input)  # Format the month
            year_input = input("Enter the year (YYYY) to search: ")
            year_input = format_year(year_input)  # Format the year
            results = search_by_month_and_year(conn, month_input, year_input)
            if results:
                print("Search Results:")
                for row in results:
                    print(row)
            else:
                print("No results found for the given month and year.")

        elif choice == '6':
            mini_plot_to_search = input("Enter the Mini_Plot to search: ")
            mini_plot_to_search = format_mini_plot(mini_plot_to_search)  # Format the Mini_Plot
            results = search_mini_plot(conn, mini_plot_to_search)
            if results:
                print("Search Results:")
                for row in results:
                    print(row)
            else:
                print("No results found for the given Mini_Plot.")

        elif choice == '7':
            handle_duplicates(conn)

        elif choice == '8':
            print("Exiting the program.")
            break

        else:
            print("Invalid option. Please try again.")

    conn.close()

# Main execution starts here
if __name__ == "__main__":
    main_menu()