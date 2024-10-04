import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog
from ttkthemes import ThemedTk
from tkinter import ttk
import pandas as pd

# Database query functions
def search_parcela_site(conn, Parcela_Site):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM post_soil_flux WHERE plot_code = ?", (Parcela_Site,))
    results = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    cursor.close()
    return results, column_names

def search_site(conn, Site):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM post_soil_flux WHERE Site = ?", (Site,))
    results = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    cursor.close()
    return results, column_names

def search_by_month(conn, month):
    cursor = conn.cursor()
    query = "SELECT * FROM post_soil_flux WHERE strftime('%m', smpl_date) = ?"
    cursor.execute(query, (month,))
    results = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    cursor.close()
    return results, column_names

def search_by_year(conn, year):
    cursor = conn.cursor()
    query = "SELECT * FROM post_soil_flux WHERE strftime('%Y', smpl_date) = ?"
    cursor.execute(query, (year,))
    results = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    cursor.close()
    return results, column_names

def search_by_month_and_year(conn, month, year):
    cursor = conn.cursor()
    query = "SELECT * FROM post_soil_flux WHERE strftime('%m', smpl_date) = ? AND strftime('%Y', smpl_date) = ?"
    cursor.execute(query, (month, year))
    results = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    cursor.close()
    return results, column_names

def search_mini_plot(conn, Miniplot):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM post_soil_flux WHERE sub_plot = ?", (Miniplot,))
    results = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    cursor.close()
    return results, column_names

# Duplicate handling
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

def list_duplicate_rows(conn, plot_code, sub_plot, CH4_finalflux_mgC_per_hr_m2):
    cursor = conn.cursor()
    cursor.execute('''SELECT rowid, * FROM post_soil_flux WHERE plot_code = ? AND sub_plot = ? AND CH4_finalflux_mgC_per_hr_m2 = ?''',
                   (plot_code, sub_plot, CH4_finalflux_mgC_per_hr_m2))
    rows = cursor.fetchall()
    cursor.close()
    return rows

def delete_row(conn, rowid):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM post_soil_flux WHERE rowid = ?", (rowid,))
    conn.commit()
    cursor.close()

def handle_duplicates(conn):
    duplicates = find_duplicates(conn)
    if not duplicates:
        messagebox.showinfo("No Duplicates", "No duplicate rows found.")
        return

    for dup in duplicates:
        plot_code, sub_plot, CH4_finalflux_mgC_per_hr_m2, count = dup
        response = messagebox.askyesno("Duplicate Found", 
            f"Duplicate set found: plot_code={plot_code}, sub_plot={sub_plot}, CH4_finalflux_mgC_per_hr_m2={CH4_finalflux_mgC_per_hr_m2}. Do you want to delete one?")
        
        if response:  # If user chooses to delete
            rows = list_duplicate_rows(conn, plot_code, sub_plot, CH4_finalflux_mgC_per_hr_m2)
            if rows:
                delete_row(conn, rows[0][0])  # Delete first row
                messagebox.showinfo("Deleted", "A duplicate row has been deleted.")
            else:
                messagebox.showinfo("Error", "No rows found to delete.")

# Function to display results in a Treeview (row and column format)
def show_results(tree, results, column_names):
    # Clear existing rows
    for row in tree.get_children():
        tree.delete(row)
    
    if results:
        tree["columns"] = column_names
        tree["show"] = "headings"
        
        # Set up column headers
        for col in column_names:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")

        # Insert rows
        for row in results:
            tree.insert("", tk.END, values=row)

        # Update the scroll region to ensure scrollbars are active
        tree.update_idletasks()

    else:
        messagebox.showinfo("No Results", "No matching records found.")

# GUI Setup
def create_gui():
    conn = sqlite3.connect("/Users/sanskarsrivastava/Desktop/CSE/Database-job/post_soil_flux.db")  # Replace with your actual database path
    
    root = ThemedTk(theme="breeze")
    root.title("Soil Flux Database")

    title_label = ttk.Label(root, text="Soil Flux Database Menu", font=("Helvetica", 18))
    title_label.pack(pady=20)

    # Create a frame for the Treeview and Scrollbars
    columns_frame = ttk.Frame(root)
    columns_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    # Create Treeview for displaying results
    tree = ttk.Treeview(columns_frame)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Scrollbars
    y_scrollbar = ttk.Scrollbar(columns_frame, orient=tk.VERTICAL, command=tree.yview)
    y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    x_scrollbar = ttk.Scrollbar(root, orient=tk.HORIZONTAL, command=tree.xview)
    x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

    # Define button actions
    def option_1():
        parcela_site = simpledialog.askstring("Input", "Enter the Parcela_Site to search:")
        results, column_names = search_parcela_site(conn, parcela_site)
        show_results(tree, results, column_names)

    def option_2():
        site = simpledialog.askstring("Input", "Enter the Site to search:")
        results, column_names = search_site(conn, site)
        show_results(tree, results, column_names)

    def option_3():
        month = simpledialog.askstring("Input", "Enter the month (MM) to search:")
        results, column_names = search_by_month(conn, month)
        show_results(tree, results, column_names)

    def option_4():
        year = simpledialog.askstring("Input", "Enter the year (YYYY) to search:")
        results, column_names = search_by_year(conn, year)
        show_results(tree, results, column_names)

    def option_5():
        month = simpledialog.askstring("Input", "Enter the month (MM) to search:")
        year = simpledialog.askstring("Input", "Enter the year (YYYY) to search:")
        results, column_names = search_by_month_and_year(conn, month, year)
        show_results(tree, results, column_names)

    def option_6():
        mini_plot = simpledialog.askstring("Input", "Enter the Mini_Plot to search:")
        results, column_names = search_mini_plot(conn, mini_plot)
        show_results(tree, results, column_names)

    def option_7():
        handle_duplicates(conn)

    # Create buttons
    buttons_frame = ttk.Frame(root)
    buttons_frame.pack(pady=20)

    ttk.Button(buttons_frame, text="1. Search by Parcela_Site", command=option_1).pack(pady=5)
    ttk.Button(buttons_frame, text="2. Search by Site", command=option_2).pack(pady=5)
    ttk.Button(buttons_frame, text="3. Search by Month", command=option_3).pack(pady=5)
    ttk.Button(buttons_frame, text="4. Search by Year", command=option_4).pack(pady=5)
    ttk.Button(buttons_frame, text="5. Search by Month and Year", command=option_5).pack(pady=5)
    ttk.Button(buttons_frame, text="6. Search by Mini-Plot", command=option_6).pack(pady=5)
    ttk.Button(buttons_frame, text="7. Check for Duplicates", command=option_7).pack(pady=5)

    root.mainloop()

create_gui()
