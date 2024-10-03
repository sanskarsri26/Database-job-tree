import tkinter as tk
from tkinter import messagebox
import sqlite3

# Function to search the database
def search_database():
    search_query = entry.get()
    
    # Connect to the SQLite database
    connection = sqlite3.connect('/Users/sanskarsrivastava/Desktop/CSE/Database-job/post_soil_flux.db')
    cursor = connection.cursor()
    
    # Execute a search query
    cursor.execute("SELECT * FROM flux_data WHERE sub_plot LIKE ?", (f"%{search_query}%",))
    
    # Fetch all results
    results = cursor.fetchall()
    
    # Clear previous results
    listbox.delete(0, tk.END)
    
    # Display results
    if results:
        for row in results:
            listbox.insert(tk.END, row)
    else:
        messagebox.showinfo("Search Result", "No results found.")
    
    # Close the database connection
    connection.close()

# Create the main window
root = tk.Tk()
root.title("Database Search")

# Create and place the search label and entry
label = tk.Label(root, text="Enter search query:")
label.pack(pady=5)

entry = tk.Entry(root, width=40)
entry.pack(pady=5)

# Create and place the search button
search_button = tk.Button(root, text="Search", command=search_database)
search_button.pack(pady=5)

# Create and place the listbox to display results
listbox = tk.Listbox(root, width=50)
listbox.pack(pady=5)

# Start the GUI main loop
root.mainloop()
