import mysql.connector


def sql_instance():
    # @TODO accept config from properties file
    try:
        connection = mysql.connector.connect(
            host="localhost",
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
