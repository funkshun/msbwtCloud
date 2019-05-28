import sqlite3

def create_db(db_file):

    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    

