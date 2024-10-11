import os
import shutil
import sqlite3
import sys
import subprocess
import csv  # Import CSV module
from datetime import datetime
from PyQt5 import QtWidgets, QtCore

# Pagination constants
ROWS_PER_PAGE = 50


class SoilFluxDatabaseApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.db_path = "/Users/sanskarsrivastava/Desktop/CSE/Database-job/post_soil_flux.db"  # Update this path
        self.conn = sqlite3.connect(self.db_path)
        self.results = []
        self.current_page = 0

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

        # Title Label
        self.title_label = QtWidgets.QLabel("Select a Option:", self)
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

    def create_search_dialog(self, option):
        def inner():
            if option == "8. Backup Database":  # Handle the backup option separately
                self.backup_database()
                self.open_db_browser()  # Open DB Browser after backup
                return
            elif option == "9. Export Search Results as CSV":  # Handle CSV export
                self.export_csv()
                return

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

    def update_table(self, column_names):
        self.table.clear()
        self.table.setColumnCount(len(column_names))
        self.table.setHorizontalHeaderLabels(column_names)

        if not self.results:
            return

        # Set the number of rows for the current page
        num_rows = min(
            ROWS_PER_PAGE, len(self.results) - self.current_page * ROWS_PER_PAGE
        )
        self.table.setRowCount(num_rows)

        # Fill the table with data for the current page
        for row_idx in range(num_rows):
            for col_idx in range(len(column_names)):
                self.table.setItem(
                    row_idx,
                    col_idx,
                    QtWidgets.QTableWidgetItem(
                        str(
                            self.results[self.current_page * ROWS_PER_PAGE + row_idx][
                                col_idx
                            ]
                        )
                    ),
                )

    def next_page(self):
        if (self.current_page + 1) * ROWS_PER_PAGE < len(self.results):
            self.current_page += 1
            self.update_table(
                [
                    description[0]
                    for description in self.conn.execute(
                        "SELECT * FROM post_soil_flux"
                    ).description
                ]
            )

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_table(
                [
                    description[0]
                    for description in self.conn.execute(
                        "SELECT * FROM post_soil_flux"
                    ).description
                ]
            )

    def export_csv(self):
        if not self.results:  # Check if no search results are available
            response = QtWidgets.QMessageBox.question(
                self,
                "Export All Data",
                "No search results available. Do you want to export the entire database?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            )

            if response == QtWidgets.QMessageBox.Yes:
                # Fetch all data from the database
                cursor = self.conn.cursor()
                cursor.execute("SELECT * FROM post_soil_flux")
                self.results = cursor.fetchall()
                column_names = [description[0] for description in cursor.description]
                cursor.close()
            else:
                return

        # Define the CSV filename and path
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"exported_data_{current_time}.csv"
        csv_path = os.path.join(os.path.dirname(self.db_path), csv_filename)

        # Write the data (either search results or the whole table) to a CSV file
        with open(csv_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(column_names)
            writer.writerows(self.results)

        QtWidgets.QMessageBox.information(
            self, "Export Successful", f"Results exported to {csv_path}"
        )

    def handle_duplicates(self):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT plot_code, COUNT(*) FROM post_soil_flux GROUP BY plot_code HAVING COUNT(*) > 1"
        )
        duplicates = cursor.fetchall()
        if not duplicates:
            QtWidgets.QMessageBox.information(
                self, "No Duplicates", "No duplicate entries found."
            )
        else:
            duplicate_msg = "\n".join(
                [f"{row[0]}: {row[1]} duplicates" for row in duplicates]
            )
            QtWidgets.QMessageBox.warning(self, "Duplicates Found", duplicate_msg)

    def backup_database(self):
        db_directory = os.path.dirname(self.db_path)
        backup_path = os.path.join(
            db_directory, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        )
        shutil.copy2(self.db_path, backup_path)
        QtWidgets.QMessageBox.information(
            self, "Backup Successful", f"Database backed up to {backup_path}"
        )

    def open_db_browser(self):
        try:
            subprocess.run(["open", "-a", "DB Browser for SQLite", self.db_path])
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e))


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = SoilFluxDatabaseApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
