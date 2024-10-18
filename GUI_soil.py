import os
import shutil
import sqlite3
import sys
import subprocess
import csv
from datetime import datetime
from PyQt5 import QtWidgets, QtCore

# Pagination constants
ROWS_PER_PAGE = 50


class SoilFluxDatabaseApp(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.db_path = self.select_database()  # Open file dialog to select database
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
        self.setGeometry(100, 100, 800, 600)

        # Create menu bar
        menubar = QtWidgets.QMenuBar(self)
        file_menu = menubar.addMenu("File")

        # Add "Open DB Browser" action
        open_db_action = QtWidgets.QAction("Open DB Browser", self)
        open_db_action.triggered.connect(self.open_db_browser)
        file_menu.addAction(open_db_action)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setMenuBar(menubar)

        # Dropdown for column selection (Full Column / Selected Column)
        self.column_selection_combo = QtWidgets.QComboBox(self)
        self.column_selection_combo.addItems(["Full Column", "Selected Column"])
        self.column_selection_combo.setCurrentIndex(0)  # Default to Full Column

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

        self.next_button = QtWidgets.QPushButton("Next", self)
        self.next_button.clicked.connect(self.next_page)
        self.navigation_layout.addWidget(self.next_button)

        self.layout.addLayout(self.navigation_layout)
        self.setLayout(self.layout)

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
                self.backup_database()
                self.open_db_browser()  # Open DB Browser after backup
                return
            elif option == "9. Export Search Results as CSV":  # Handle CSV export
                self.export_csv()
                return
            elif option == "7. Check for Duplicates":  # Directly check for duplicates
                self.handle_duplicates()
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
        cursor.execute("SELECT * FROM post_soil_flux WHERE mini_plot = ?", (mini_plot,))
        results = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        cursor.close()
        return results, column_names

    def handle_duplicates(self):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT smpl_date, sub_plot, chamber, COUNT(*) as count FROM post_soil_flux GROUP BY smpl_date, sub_plot, chamber HAVING count > 1"
        )
        duplicates = cursor.fetchall()

        if not duplicates:
            QtWidgets.QMessageBox.information(
                self, "No Duplicates", "No duplicate records found."
            )
        else:
            msg = "Duplicate records found:\n\n"
            for row in duplicates:
                msg += f"Date: {row[0]}, Plot: {row[1]}, Chamber: {row[2]}, Count: {row[3]}\n"
            QtWidgets.QMessageBox.information(self, "Duplicates", msg)

    def update_table(self, column_names):
        self.table.setRowCount(0)
        self.table.setColumnCount(len(column_names))
        self.table.setHorizontalHeaderLabels(column_names)

        start_row = self.current_page * ROWS_PER_PAGE
        end_row = start_row + ROWS_PER_PAGE
        data_to_display = self.results[start_row:end_row]

        for row_idx, row_data in enumerate(data_to_display):
            self.table.insertRow(row_idx)
            for col_idx, item in enumerate(row_data):
                self.table.setItem(
                    row_idx, col_idx, QtWidgets.QTableWidgetItem(str(item))
                )

        self.table.resizeColumnsToContents()

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_table(self.selected_columns)

    def next_page(self):
        if (self.current_page + 1) * ROWS_PER_PAGE < len(self.results):
            self.current_page += 1
            self.update_table(self.selected_columns)

    def backup_database(self):
        backup_file = f"{self.db_path}.backup"
        shutil.copy(self.db_path, backup_file)
        QtWidgets.QMessageBox.information(
            self, "Backup Successful", "Database backup created."
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

        # Add checkboxes for each column
        self.column_checkboxes = {}
        for column in self.selected_columns:
            checkbox = QtWidgets.QCheckBox(column)
            checkbox.setChecked(False)  # Default unchecked
            self.column_checkboxes[column] = checkbox
            layout.addWidget(checkbox)

        # Quick selection buttons
        select_full_button = QtWidgets.QPushButton("Select Full Columns", self)
        select_full_button.clicked.connect(self.select_full_columns)
        layout.addWidget(select_full_button)

        select_selected_button = QtWidgets.QPushButton("Select Selected Columns", self)
        select_selected_button.clicked.connect(self.select_selected_columns)
        layout.addWidget(select_selected_button)

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
                self.save_to_csv(file_name, selected_columns)
                QtWidgets.QMessageBox.information(
                    self, "Export Successful", "Data exported successfully."
                )
        dialog.close()

    def save_to_csv(self, file_name, selected_columns):
        # Get the column names from the current results
        if self.results:
            column_names = [
                description[0]
                for description in self.conn.execute(
                    "SELECT * FROM post_soil_flux"
                ).description
            ]

            # Create a mapping from column name to index
            col_index_map = {name: index for index, name in enumerate(column_names)}

            with open(file_name, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(selected_columns)  # Write headers

                for row in self.results:
                    # Use the mapping to access the correct indices
                    writer.writerow(
                        [
                            row[col_index_map[col]]
                            for col in selected_columns
                            if col in col_index_map
                        ]
                    )  # Write selected data


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SoilFluxDatabaseApp()
    window.show()
    sys.exit(app.exec_())
