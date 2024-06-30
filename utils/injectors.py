import mysql.connector
from mysql.connector import MySQLConnection


def sql_instance() -> MySQLConnection:
    """
    Establish a connection to the MySQL database and return the connection object.

    Returns:
        MySQLConnection: A connection object to the MySQL database if successful, None otherwise.

    Raises:
        mysql.connector.Error: If there is an error in connecting to the database.
    """
    # @TODO accept config from properties file
    try:
        connection = mysql.connector.connect(
            host="db",
            user="mysql",
            password="mysqlpwd",
            database="doctor_patient_db",
        )
        if connection.is_connected():
            print("Connected to database")
            return connection
    except mysql.connector.Error as e:
        print("Error connection to database", str(e))
        return None
