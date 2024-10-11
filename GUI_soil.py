import sqlite3
import sys
from PyQt5 import QtWidgets, QtCore

# Pagination constants
ROWS_PER_PAGE = 50


class SoilFluxDatabaseApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.conn = sqlite3.connect(
            "/Users/sanskarsrivastava/Desktop/CSE/Database-job/post_soil_flux.db"
        )  # Update this path
        self.results = []
        self.current_page = 0

    def init_ui(self):
        self.setWindowTitle("Soil Flux Database")
        self.setGeometry(100, 100, 800, 600)

        # Layout
        self.layout = QtWidgets.QVBoxLayout()

        # Title Label
        self.title_label = QtWidgets.QLabel("Select a Search Option:", self)
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

    def find_duplicates(self):
        cursor = self.conn.cursor()
        query = """
            SELECT plot_code, sub_plot, CH4_finalflux_mgC_per_hr_m2, COUNT(*) as count
            FROM post_soil_flux
            GROUP BY plot_code, sub_plot, CH4_finalflux_mgC_per_hr_m2
            HAVING COUNT(*) > 1
        """
        cursor.execute(query)
        duplicates = cursor.fetchall()
        cursor.close()
        return duplicates

    def list_duplicate_rows(self, plot_code, sub_plot, CH4_finalflux_mgC_per_hr_m2):
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT rowid, * FROM post_soil_flux WHERE plot_code = ? AND sub_plot = ? AND CH4_finalflux_mgC_per_hr_m2 = ?""",
            (plot_code, sub_plot, CH4_finalflux_mgC_per_hr_m2),
        )
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def delete_row(self, rowid):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM post_soil_flux WHERE rowid = ?", (rowid,))
        self.conn.commit()
        cursor.close()

    def handle_duplicates(self):
        duplicates = self.find_duplicates()
        if not duplicates:
            QtWidgets.QMessageBox.information(
                self, "No Duplicates", "No duplicate rows found."
            )
            return

        for dup in duplicates:
            plot_code, sub_plot, CH4_finalflux_mgC_per_hr_m2, count = dup
            response = QtWidgets.QMessageBox.question(
                self,
                "Duplicate Found",
                f"Duplicate set found: plot_code={plot_code}, sub_plot={sub_plot}, CH4_finalflux_mgC_per_hr_m2={CH4_finalflux_mgC_per_hr_m2}. Do you want to delete one?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            )

            if response == QtWidgets.QMessageBox.Yes:
                rows = self.list_duplicate_rows(
                    plot_code, sub_plot, CH4_finalflux_mgC_per_hr_m2
                )
                if rows:
                    self.delete_row(rows[0][0])  # Deletes the first found duplicate
                    QtWidgets.QMessageBox.information(
                        self, "Deleted", "One duplicate row has been deleted."
                    )
                else:
                    QtWidgets.QMessageBox.warning(
                        self, "Error", "No rows found for deletion."
                    )

    def closeEvent(self, event):
        self.conn.close()
        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SoilFluxDatabaseApp()
    window.show()
    sys.exit(app.exec_())
