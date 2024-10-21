import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="hola123",
        database="alumnat"
    )
    return connection
