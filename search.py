import sqlite3

def search_parcela_site(cursor):
    search_input = input("Enter the Parcela Site to search for: ")
    cursor.execute("SELECT * FROM tree_data WHERE Parcela_Site LIKE ?", ('%' + search_input + '%',))
    results = cursor.fetchall()

    if results:
        for row in results:
            print(row)
    else:
        print("No matches found.")

def search_by_month(cursor):
    month_input = input("Enter the month (MM) to search for: ")
    cursor.execute("SELECT * FROM tree_data WHERE strftime('%m', fecha) = ?", (month_input,))
    results = cursor.fetchall()

    if results:
        for row in results:
            print(row)
    else:
        print("No matches found.")

def search_by_year(cursor):
    year_input = input("Enter the year (YYYY) to search for: ")
    cursor.execute("SELECT * FROM tree_data WHERE strftime('%Y', fecha) = ?", (year_input,))
    results = cursor.fetchall()

    if results:
        for row in results:
            print(row)
    else:
        print("No matches found.")

def search_by_month_and_year(cursor):
    month_input = input("Enter the month (MM) to search for: ")
    year_input = input("Enter the year (YYYY) to search for: ")
    cursor.execute("SELECT * FROM tree_data WHERE strftime('%m', fecha) = ? AND strftime('%Y', fecha) = ?", (month_input, year_input))
    results = cursor.fetchall()

    if results:
        for row in results:
            print(row)
    else:
        print("No matches found.")

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('/Users/sanskarsrivastava/Desktop/CSE/Database-job/tree_data.db')  # Corrected path
    cursor = conn.cursor()

    while True:
        print("\nMenu:")
        print("1) Search Parcela Site")
        print("2) Search by Month")
        print("3) Search by Year")
        print("4) Search by Month and Year")
        print("5) Exit")

        choice = input("Choose an option (1-5): ")

        if choice == '1':
            search_parcela_site(cursor)
        elif choice == '2':
            search_by_month(cursor)
        elif choice == '3':
            search_by_year(cursor)
        elif choice == '4':
            search_by_month_and_year(cursor)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()
