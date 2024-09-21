import mysql.connector
from mysql.connector import errorcode

# Define the database connection parameters
config = {
    'user': 'root',
    'password': 'qwerty12345',
    'host': '127.0.0.1',
    'database': 'my_database',
    'raise_on_warnings': True
}

try:
    # Establish a connection to the database
    cnx = mysql.connector.connect(**config)

    # Create a cursor object to execute queries
    cursor = cnx.cursor()

    # Get the search term from user input
    search_term = input("Enter a search term: ")

    # Prepare the query
    query = ("SELECT * FROM tree_data "
             "WHERE MATCH(especie_arbol, nombre_colectores, notas) "
             "AGAINST (%s IN NATURAL LANGUAGE MODE)")

        # Execute the query
    cursor.execute(query, (search_term,))

    # Fetch the results
    results = cursor.fetchall()

    # Check if any results were found
    if results:
        for row in results:
            print(row)  # Print each row of results
    else:
        print("No results found.")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist.")
    else:
        print(err)

finally:
    # Close the cursor and connection
    cursor.close()
    cnx.close()