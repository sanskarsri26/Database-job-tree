import os
import shutil
import sqlite3
import sys
import subprocess
import csv
from datetime import datetime
from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QComboBox,
    QPushButton,
    QLabel,
    QMessageBox,
)

# Pagination constants
ROWS_PER_PAGE = 50


class MultiSearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Multiple Search")
        self.setGeometry(100, 100, 400, 400)  

        # Layout
        layout = QVBoxLayout()

        # Dropdowns for column selection
        self.column1_dropdown = QComboBox(self)
        self.column2_dropdown = QComboBox(self)
        self.column3_dropdown = QComboBox(self)
        self.column4_dropdown = QComboBox(self)
        self.column5_dropdown = QComboBox(self)  # Fifth dropdown

        # Populate dropdowns with column names from the database
        column_names = parent.get_column_names_from_db_2("post_soil_flux")
        column_names.insert(0, "None")  # Add "None" as the first option
        self.column1_dropdown.addItems(column_names)
        self.column2_dropdown.addItems(column_names)
        self.column3_dropdown.addItems(column_names)
        self.column4_dropdown.addItems(column_names)
        self.column5_dropdown.addItems(column_names)  # Populate fifth dropdown

        # Add dropdowns to layout
        layout.addWidget(QLabel("Select First Column:"))
        layout.addWidget(self.column1_dropdown)
        layout.addWidget(QLabel("Select Second Column:"))
        layout.addWidget(self.column2_dropdown)
        layout.addWidget(QLabel("Select Third Column:"))
        layout.addWidget(self.column3_dropdown)
        layout.addWidget(QLabel("Select Fourth Column:"))
        layout.addWidget(self.column4_dropdown)
        layout.addWidget(QLabel("Select Fifth Column:"))  # Label for fifth column
        layout.addWidget(self.column5_dropdown)

        # Search button
        search_button = QPushButton("Search", self)
        search_button.clicked.connect(self.perform_search)

        # Add button to layout
        layout.addWidget(search_button)

        self.setLayout(layout)

    def perform_search(self):
        column1 = self.column1_dropdown.currentText()
        column2 = self.column2_dropdown.currentText()
        column3 = self.column3_dropdown.currentText()
        column4 = self.column4_dropdown.currentText()
        column5 = self.column5_dropdown.currentText()  # Get fifth column

        # Get criteria from user input
        criteria1, ok1 = (
            QtWidgets.QInputDialog.getText(
                self, "Input", f"Enter criteria for {column1}:"
            )
            if column1 != "None"
            else (None, True)
        )  # Skip input if "None"

        criteria2, ok2 = (
            QtWidgets.QInputDialog.getText(
                self, "Input", f"Enter criteria for {column2}:"
            )
            if column2 != "None"
            else (None, True)
        )  # Skip input if "None"

        criteria3, ok3 = (
            QtWidgets.QInputDialog.getText(
                self, "Input", f"Enter criteria for {column3}:"
            )
            if column3 != "None"
            else (None, True)
        )  # Skip input if "None"

        criteria4, ok4 = (
            QtWidgets.QInputDialog.getText(
                self, "Input", f"Enter criteria for {column4}:"
            )
            if column4 != "None"
            else (None, True)
        )  # Skip input if "None"

        criteria5, ok5 = (
            QtWidgets.QInputDialog.getText(
                self, "Input", f"Enter criteria for {column5}:"
            )
            if column5 != "None"
            else (None, True)
        )  # Skip input if "None"

        # Validate that input was given for columns that are not "None"
        if (
            ok1
            and (column1 == "None" or criteria1)
            and ok2
            and (column2 == "None" or criteria2)
            and ok3
            and (column3 == "None" or criteria3)
            and ok4
            and (column4 == "None" or criteria4)
            and ok5
            and (column5 == "None" or criteria5)
        ):

            # Call the parent's search function
            self.parent().perform_multiple_search(
                column1,
                criteria1,
                column2,
                criteria2,
                column3,
                criteria3,
                column4,
                criteria4,
                column5,
                criteria5,
            )
            self.close()


class SoilFluxDatabaseApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.username = self.prompt_username()
        self.log_username()
        self.db_path = self.select_database()
        self.conn = sqlite3.connect(self.db_path)
        self.results = []
        self.current_page = 0

        # Define selected columns
        self.selected_columns = [
            "smpl_date",
            "sub_plot",
            "chamber",
            "LICOR_CO2_data_file_name",
            "raw_start_time",
            "raw_end_time",
            "air_temp_c",
            "atmp_Kpa",
            "soil_temp_c",
            "ave_collar_height",
            "water_height_above_soil",
            "floating_chamber_used",
            "floating_collar_height",
            "flooded_chamber",
            "flooded_site",
            "site_comments",
            "date_time",
            "ave_pH",
            "instr",
            "field_workers",
            "Final_CH4_flux_category",
            "Final_CO2_flux_category",
            "Final_CO2_file_status",
            "CH4_rsquared",
            "CO2_rsquared",
            "CH4_exp_rsquared",
            "CO2_exp_rsquared",
            "CH4_fieldflux_mgC_per_hr_m2_linear",
            "CH4_fieldflux_mgC_per_hr_m2_exponential",
            "CO2_fieldflux_mgC_per_hr_m2_linear",
            "CO2_fieldflux_mgC_per_hr_m2_exponential",
            "No_QAQC_CH4_finalflux_mgC_per_hr_m2",
            "No_QAQC_CO2_finalflux_mgC_per_hr_m2",
            "Final_CH4_flux_valid_or_not",
            "Final_CO2_flux_valid_or_not",
            "CH4_finalflux_mgC_per_hr_m2",
            "CO2_finalflux_mgC_per_hr_m2",
        ]

    def init_ui(self):
        self.setWindowTitle("Soil Flux Database")
        self.setGeometry(300, 300, 800, 600)

        # Create menu bar
        menubar = QtWidgets.QMenuBar(self)
        file_menu = menubar.addMenu("File")

        # Add "Open DB Browser" action
        open_db_action = QtWidgets.QAction("Open DB Browser", self)
        open_db_action.triggered.connect(self.open_db_browser)
        file_menu.addAction(open_db_action)

        self.top_row_layout = QtWidgets.QHBoxLayout()  # Create a horizontal layout for the top row

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setMenuBar(menubar)

        # Dropdown for column selection (Full Column / Selected Column)
        self.column_selection_combo = QtWidgets.QComboBox(self)
        self.column_selection_combo.addItems(["Full Column", "Selected Column"])
        self.column_selection_combo.setCurrentIndex(0)  # Default to Full Column
        self.top_row_layout.addWidget(self.column_selection_combo)  # Add the dropdown to the top row layout

        # Button to show all data
        self.show_all_button = QtWidgets.QPushButton("Show All Data", self)
        self.show_all_button.clicked.connect(self.show_all_data)  # Connect to the new method
        self.top_row_layout.addWidget(self.show_all_button)  # Add the button to the top row layout

        # Layout for dropdown (positioning in top-right)
        self.dropdown_layout = QtWidgets.QHBoxLayout()
        self.dropdown_layout.addStretch(1)  # Push dropdown to the right
        self.dropdown_layout.addWidget(self.column_selection_combo)
        self.layout.addLayout(self.dropdown_layout)

        # Title Label
        self.title_label = QtWidgets.QLabel("Select an Option:", self)
        self.layout.addWidget(self.title_label)

        # Search Options
        self.option_buttons = []
        options = [
            "1. Search by Parcela_Site",
            "2. Search by Site",
            "3. Search by Month",
            "4. Search by Year",
            "5. Search by Month and Year",
            "6. Search by Mini-Plot",
            "7. Check for Duplicates",
            "8. Backup Database",
            "9. Export Search Results as CSV",
            "10. Multiple Search",
        ]

        for option in options:
            button = QtWidgets.QPushButton(option, self)
            button.clicked.connect(self.create_search_dialog(option))
            self.layout.addWidget(button)
            self.option_buttons.append(button)

        # Table for displaying results
        self.table = QtWidgets.QTableWidget(self)
        self.layout.addWidget(self.table)

        # Navigation Buttons
        self.navigation_layout = QtWidgets.QHBoxLayout()
        self.prev_button = QtWidgets.QPushButton("Previous", self)
        self.prev_button.clicked.connect(self.previous_page)
        self.navigation_layout.addWidget(self.prev_button)

        self.table.horizontalHeader().setStretchLastSection(True)

        self.next_button = QtWidgets.QPushButton("Next", self)
        self.next_button.clicked.connect(self.next_page)
        self.navigation_layout.addWidget(self.next_button)

        self.layout.addLayout(self.navigation_layout)
        self.setLayout(self.layout)

    def show_all_data(self):
        # Fetch all records from the database
        query = "SELECT * FROM post_soil_flux"
        self.results = self.perform_query(query, ())  # Call perform_query without parameters

        if self.results:
            column_names = self.get_column_names_from_db('post_soil_flux')  # Fetch column names
            self.update_table(column_names)  # Update the table to show all data
        else:
            QtWidgets.QMessageBox.warning(self, "No Data", "No records found in the database.")

    def closeEvent(self, event):
        # Save the database with a timestamped filename
        self.save_database_on_exit()
        event.accept()  # Accept the event to close the window

    def save_database_on_exit(self):
        try:
            # Create a filename with current date and time
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = f"saved_data_{timestamp}.db"
            # Copy the database to a new file
            shutil.copy2(self.db_path, backup_file)
            QtWidgets.QMessageBox.information(
                self, "Save Successful", f"Database saved as: {backup_file}"
            )
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, "Save Failed", f"Failed to save database: {str(e)}"
            )

    def on_username_changed(self, text):
        self.username = text
        self.log_area.append(
            f"Username changed to {text} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

    def select_database(self):
        db_file, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select SQLite Database",
            "",
            "SQLite Database Files (*.db);;All Files (*)",
        )
        if not db_file:
            QtWidgets.QMessageBox.critical(self, "Error", "No database selected!")
            sys.exit(1)  # Exit if no database is selected
        return db_file

    def create_search_dialog(self, option):
        def inner():
            if option == "8. Backup Database":  # Handle the backup option separately
                self.prompt_and_log_changes()
                self.backup_database()
                self.open_db_browser()  # Open DB Browser after backup
                return
            elif option == "9. Export Search Results as CSV":  # Handle CSV export
                self.export_csv()
                return
            elif option == "7. Check for Duplicates":  # Directly check for duplicates
                self.handle_duplicates()
                return
            elif option == "10. Multiple Search":  # Directly handle multiple search
                dialog = MultiSearchDialog(self)
                dialog.exec_()
                return

            # For other options, prompt for input
            search_term, ok = QtWidgets.QInputDialog.getText(
                self, "Input", f"Enter value for {option}:"
            )
            if ok and search_term:
                self.perform_search(option, search_term)

        return inner

    def perform_search(self, option, search_term):
        if option == "1. Search by Parcela_Site":
            self.results, column_names = self.search_parcela_site(search_term)
        elif option == "2. Search by Site":
            self.results, column_names = self.search_site(search_term)
        elif option == "3. Search by Month":
            self.results, column_names = self.search_by_month(search_term)
        elif option == "4. Search by Year":
            self.results, column_names = self.search_by_year(search_term)
        elif option == "5. Search by Month and Year":
            month, ok1 = QtWidgets.QInputDialog.getText(
                self, "Input", "Enter month (MM):"
            )
            if ok1:
                year, ok2 = QtWidgets.QInputDialog.getText(
                    self, "Input", "Enter year (YYYY):"
                )
                if ok2:
                    self.results, column_names = self.search_by_month_and_year(
                        month, year
                    )
        elif option == "6. Search by Mini-Plot":
            self.results, column_names = self.search_mini_plot(search_term)
        elif option == "7. Check for Duplicates":
            self.handle_duplicates()
            return

        if not self.results:
            QtWidgets.QMessageBox.information(
                self, "No Results", "No matching records found."
            )
            return

        self.current_page = 0
        selected_option = self.column_selection_combo.currentText()

        if selected_option == "Full Column":
            column_names = [
                description[0]
                for description in self.conn.execute(
                    "SELECT * FROM post_soil_flux"
                ).description
            ]
        else:  # "Selected Column"
            column_names = self.selected_columns

        self.update_table(column_names)

    def search_parcela_site(self, parcela_site):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM post_soil_flux WHERE plot_code = ?", (parcela_site,)
        )
        results = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        cursor.close()
        return results, column_names

    def search_site(self, site):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM post_soil_flux WHERE Site = ?", (site,))
        results = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        cursor.close()
        return results, column_names

    def search_by_month(self, month):
        cursor = self.conn.cursor()
        query = "SELECT * FROM post_soil_flux WHERE strftime('%m', smpl_date) = ?"
        cursor.execute(query, (month,))
        results = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        cursor.close()
        return results, column_names

    def search_by_year(self, year):
        cursor = self.conn.cursor()
        query = "SELECT * FROM post_soil_flux WHERE strftime('%Y', smpl_date) = ?"
        cursor.execute(query, (year,))
        results = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        cursor.close()
        return results, column_names

    def search_by_month_and_year(self, month, year):
        cursor = self.conn.cursor()
        query = "SELECT * FROM post_soil_flux WHERE strftime('%m', smpl_date) = ? AND strftime('%Y', smpl_date) = ?"
        cursor.execute(query, (month, year))
        results = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        cursor.close()
        return results, column_names

    def search_mini_plot(self, mini_plot):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM post_soil_flux WHERE sub_plot = ?", (mini_plot,))
        results = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        cursor.close()
        return results, column_names

    def handle_duplicates(self):
        cursor = self.conn.cursor()
        # Query to find duplicates based on smpl_date, sub_plot, and chamber
        cursor.execute(
            """
            SELECT rowid, smpl_date, sub_plot, chamber
            FROM post_soil_flux
            WHERE (smpl_date, sub_plot, chamber) IN (
                SELECT smpl_date, sub_plot, chamber
                FROM post_soil_flux
                GROUP BY smpl_date, sub_plot, chamber
                HAVING COUNT(*) > 1
            )
            ORDER BY smpl_date, sub_plot, chamber
            """
        )
        duplicates = cursor.fetchall()

        if not duplicates:
            QtWidgets.QMessageBox.information(
                self, "No Duplicates", "No duplicate records found."
            )
        else:
            msg = "Duplicate records found:\n\n"
            current_key = None

            for row in duplicates:
                key = (row[1], row[2], row[3])  # (smpl_date, sub_plot, chamber)
                if key != current_key:
                    if current_key is not None:
                        msg += "\n"  # Separate different groups of duplicates
                    current_key = key
                    msg += f"Date: {row[1]}, Plot: {row[2]}, Chamber: {row[3]}\n"

                msg += f"  - Row ID: {row[0]}\n"

            msg += "\nPlease resolve these duplicates by reviewing the data."
            QtWidgets.QMessageBox.information(self, "Duplicates", msg)

        cursor.close()

    def update_table(self, column_names=None):
        # Fetch all columns if not provided
        if column_names is None:
            column_names = self.get_column_names_from_db('post_soil_flux')  # Ensure you're getting the right columns

        # Set the row and column count
        self.table.setRowCount(0)
        self.table.setColumnCount(len(column_names))
        self.table.setHorizontalHeaderLabels(column_names)

        # Display data in paginated view or all data if pagination is not needed
        start_row = self.current_page * ROWS_PER_PAGE
        end_row = start_row + ROWS_PER_PAGE

        # If you want to display all results without pagination, you can comment the next line
        data_to_display = self.results[start_row:end_row]

        # If you want to display all results regardless of pagination
        # data_to_display = self.results

        for row_idx, row_data in enumerate(data_to_display):
            self.table.insertRow(row_idx)
            for col_idx, item in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(item)))

        # Resize columns to fit content
        self.table.resizeColumnsToContents()

    def prompt_and_log_changes(self):
        # Prompt for username
        username, ok1 = QtWidgets.QInputDialog.getText(self, 'Username Input', 'Enter your username:')
        if not ok1 or not username:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Username is required.")
            return

        # Prompt for changes
        changes, ok2 = QtWidgets.QInputDialog.getText(self, 'Changes Input', 'Describe the changes you made:')
        if not ok2 or not changes:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Description of changes is required.")
            return

        # Log the information
        log_entry = f"Username: {username}, Changes: {changes}, Date & Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        with open('changes_log.txt', 'a') as log_file:
            log_file.write(log_entry)

        QtWidgets.QMessageBox.information(self, "Log Successful", "Your changes have been logged successfully.")

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_table(self.selected_columns)

    def next_page(self):
        if (self.current_page + 1) * ROWS_PER_PAGE < len(self.results):
            self.current_page += 1
            self.update_table(self.selected_columns)

    def backup_database(self):
        try:
            backup_file = (
                f"{self.db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            )
            shutil.copy2(self.db_path, backup_file)
            QtWidgets.QMessageBox.information(
                self, "Backup Successful", f"Database backup created: {backup_file}"
            )
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, "Backup Failed", f"Failed to create backup: {str(e)}"
            )

    def open_db_browser(self):
        db_browser_path = "/Applications/DB Browser for SQLite.app"
        subprocess.call(["open", db_browser_path])

    def export_csv(self):
        # Create an export dialog for column selection
        column_dialog = QtWidgets.QDialog(self)
        column_dialog.setWindowTitle("Export CSV")
        column_dialog.setGeometry(100, 100, 400, 300)

        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel("Select Columns to Export:", self)
        layout.addWidget(label)

        # Create a scroll area
        scroll_area = QtWidgets.QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # Create a widget to hold the checkboxes
        checkbox_widget = QtWidgets.QWidget()
        checkbox_layout = QtWidgets.QVBoxLayout(checkbox_widget)

        # Fetch all column names from the database table 'post_soil_flux'
        column_names = self.get_column_names_from_db('post_soil_flux')

        # Add checkboxes for each column
        self.column_checkboxes = {}
        for column in column_names:  # Use all column names fetched from the database
            checkbox = QtWidgets.QCheckBox(column)
            checkbox.setChecked(False)  # Default unchecked
            self.column_checkboxes[column] = checkbox
            checkbox_layout.addWidget(checkbox)

        # Set the layout for the checkbox widget
        checkbox_widget.setLayout(checkbox_layout)

        # Set the widget of the scroll area
        scroll_area.setWidget(checkbox_widget)
        layout.addWidget(scroll_area)

        # Quick selection buttons
        select_full_button = QtWidgets.QPushButton("Select All Columns", self)
        select_full_button.clicked.connect(self.select_full_columns)
        layout.addWidget(select_full_button)

        export_button = QtWidgets.QPushButton("Export", self)
        export_button.clicked.connect(lambda: self.confirm_export(column_dialog))
        layout.addWidget(export_button)

        column_dialog.setLayout(layout)
        column_dialog.exec_()

    def select_full_columns(self):
        for checkbox in self.column_checkboxes.values():
            checkbox.setChecked(True)  # Select all columns

    def select_selected_columns(self):
        for column in self.selected_columns:
            self.column_checkboxes[column].setChecked(
                column in self.selected_columns
            )  # Select only the selected columns

    def confirm_export(self, dialog):
        selected_columns = [
            column
            for column, checkbox in self.column_checkboxes.items()
            if checkbox.isChecked()
        ]
        if selected_columns:
            file_name, _ = QtWidgets.QFileDialog.getSaveFileName(
                self, "Save CSV", "", "CSV Files (*.csv)"
            )
            if file_name:
                self.save_to_csv(file_name, selected_columns)  # Pass selected columns correctly
                QtWidgets.QMessageBox.information(
                    self, "Export Successful", "Data exported successfully."
                )
        else:
            QtWidgets.QMessageBox.warning(
                self, "No Columns Selected", "Please select at least one column to export."
            )
        dialog.close()

    def get_column_names_from_db(self, table_name):
        """Fetches the column names from the specified table in the database."""
        try:
            # Create a cursor object using the database connection
            cursor = self.conn.cursor()

            # Execute the PRAGMA statement to get column information
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()

            # Extract column names from the fetched data
            column_names = [column[1] for column in columns]  # column[1] contains the column name

            return (column_names)

        except sqlite3.Error as e:
            print(f"An error occurred while fetching column names: {str(e)}")
            return []
        finally:
            # Ensure the cursor is closed
            cursor.close()

    def get_column_names_from_db_2(self, table_name):
        """Fetches the column names from the specified table in the database."""
        try:
            # Create a cursor object using the database connection
            cursor = self.conn.cursor()

            # Execute the PRAGMA statement to get column information
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()

            # Extract column names from the fetched data
            column_names = [
                column[1] for column in columns
            ]  # column[1] contains the column name

            return sorted(column_names)

        except sqlite3.Error as e:
            print(f"An error occurred while fetching column names: {str(e)}")
            return []
        finally:
            # Ensure the cursor is closed
            cursor.close()

    def save_to_csv(self, file_name, selected_columns):
        # Ensure there are results to export
        if not self.results:
            QtWidgets.QMessageBox.warning(
                self, "No Data", "There are no results to export."
            )
            return

        # get_column_names_from_db(self)

        # Get the column names from the database to ensure index mapping
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM post_soil_flux LIMIT 1")
        column_names = [description[0] for description in cursor.description]

        # Create a mapping from column name to index
        col_index_map = {name: index for index, name in enumerate(column_names)}

        # Open the CSV file for writing
        with open(file_name, mode="w", newline="") as file:
            writer = csv.writer(file)

            # Write the selected column headers
            writer.writerow(selected_columns)

            # Write the data rows based on selected columns
            for result in self.results:
                # Use col_index_map to fetch the correct data for each selected column
                row = [result[col_index_map[col]] for col in selected_columns if col in col_index_map]
                writer.writerow(row)

        cursor.close()

    def prompt_username(self):
        username, ok = QtWidgets.QInputDialog.getText(
            self, "Username Input", "Enter your username:"
        )
        if ok and username:
            return username
        else:
            return None  # Handle case where no username is entere

    def log_username(self):
        if self.username:
            log_entry = f"Username: {self.username} - Date & Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            with open("log.txt", "a") as log_file:
                log_file.write(log_entry)

    def perform_query(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        return results


    def perform_multiple_search(self, column1, criteria1, column2, criteria2,
                            column3, criteria3, column4, criteria4,
                            column5, criteria5):
        query = "SELECT * FROM post_soil_flux WHERE"
        conditions = []
        params = []

        # Check each column and its criteria
        for column, criteria in zip(
            [column1, column2, column3, column4, column5],
            [criteria1, criteria2, criteria3, criteria4, criteria5]
        ):
            if column != "None" and criteria:  # Ensure column is not 'None' and criteria is provided
                conditions.append(f"{column} LIKE ?")
                params.append(f"%{criteria}%")

        # Only combine conditions if any are present
        if conditions:
            query += " " + " AND ".join(conditions)  # Properly join conditions
        else:
            # If no conditions, handle this case
            QMessageBox.warning(self, "No Conditions", "At least one condition must be specified.")
            return  # Exit the method if there are no conditions

        # Debugging: print the generated query and parameters
        print("Generated Query:", query)
        print("Parameters:", params)

        # Execute the query
        results = self.perform_query(query, params)

        if results:
            self.results = results
            column_names = [
                description[0]
                for description in self.conn.execute(
                    "SELECT * FROM post_soil_flux"
                ).description
            ]
            self.update_table(column_names)
        else:
            QMessageBox.warning(
                self, "No Results", "No results found for the given criteria."
            )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SoilFluxDatabaseApp()
    window.show()
    sys.exit(app.exec_())

from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QComboBox,
    QPushButton,
    QLabel,
    QMessageBox,
)
