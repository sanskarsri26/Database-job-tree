# Soil Flux Database Management Application 

[GitHub Repository](https://github.com/sanskarsri26/Database-job-tree)

This PyQt-based application provides tools for managing a soil flux SQLite database, allowing users to search, view, export, and handle potential duplicates in the data. The application supports functionalities like performing multi-criteria searches, logging changes, backing up the database, and exporting results to CSV. 

## Features
- **Search by Month and Year**: Allows filtering records based on a specific month and year from the `smpl_date` column.
- **Search by Sub Plot**: Lets users search for records by the `sub_plot` field.
- **Duplicate Handling**: Detects duplicates based on `smpl_date`, `sub_plot`, and `chamber` fields and prompts users to review them.
- **Database Backup**: Prompts users for their username and a description of changes logged to a file. Creates a timestamped backup of the SQLite database.
- **Open DB Browser**: Opens the DB Browser for SQLite directly from the application.
- **CSV Export**: Users can select specific columns and export the search results to a CSV file.
- **Multiple Search Criteria**: Performs searches based on two criteria selected from dropdown menus for flexible querying.

## Prerequisites
Follow this repository to install all the libraries and application: [Dependency Installation](https://github.com/sanskarsri26/dependency)

1. Ensure the SQLite database file (`post_soil_flux.db`) is in the correct directory. Always ensure that the database name is `post_soil_flux.db`.
2. Run the application: `GUI_soil.py`.

### Database Path Configuration
The default database path is set to `/Users/sanskarsrivastava/Desktop/CSE/Database-job/post_soil_flux.db`. This is predefined; you need to change this according to the location you are using.

## Usage

### Search by Month and Year
1. Enter a month (MM format) and year (YYYY format).
2. Click "Search" to filter results based on the `smpl_date` column.

### Search by Sub Plot
1. Enter the `sub_plot` value in the respective field.
2. Click "Search" to get records matching the `sub_plot`.

### Handling Duplicates
1. Select the option to check for duplicates.
2. A message will display any duplicate records found, based on the combination of `smpl_date`, `sub_plot`, and `chamber`.

### Logging Changes
1. When prompted, enter your username and a description of the changes made.
2. The details will be logged in a text file (`changes_log.txt`).

### Backup the Database
1. Select the "Backup" option in the menu.
2. A backup of the database will be created with a timestamp in the same directory.

### Open DB Browser
1. From the menu, select the option to open DB Browser for SQLite.
2. The application will attempt to launch the DB Browser located at `/Applications/DB Browser for SQLite.app`.

### Exporting Data to CSV
1. Select the "Export CSV" option in the menu.
2. Choose the columns you want to export and click "Export."
3. Save the file to your desired location.

### Multiple Search Criteria
1. Open the "Multiple Search" option.
2. Select two columns and enter the criteria for each.
3. The results will be filtered based on the specified criteria.

