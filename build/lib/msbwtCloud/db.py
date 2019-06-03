import sqlite3
import json
import datetime
results_tbl_sql = \
"""
CREATE TABLE IF NOT EXISTS tasks (
    id integer PRIMARY KEY,
    token text NOT NULL,
    json text NOT NULL,
    start_date text NOT NULL
    );
"""
def create_db(db_file):

    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute(results_tbl_sql)
        conn.commit()
        #return conn
    except Exception as e:
        print(e)

def connect_db(db_file):
    try:
        conn = sqlite3.connect(db_file)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(e)
        return None

def insert_task(conn, token, dic, date_str):

    insert_token_sql = \
    """
        INSERT INTO tasks(token, json, start_date) VALUES(?,?,?);
    """
   
    try:
        dic['date'] = dic['date'].strftime('%Y-%m-%d %H:%M:%S')
        vals = (token, json.dumps(dic), date_str)
        c = conn.cursor()
        c.execute(insert_token_sql, vals)
        conn.commit()
        return c.lastrowid
    except Exception as e:
        print(e)
        return None

def retrieve_token(conn, token):

    retrieve_token_sql = \
        """
            SELECT * FROM tasks WHERE token = ?;
        """

    try:
        c = conn.cursor()
        c.execute(retrieve_token_sql, (token.decode('ascii'),))
        rows = c.fetchall()
        #print(len(rows))
        return json.loads(rows[0][2])

    except Exception as e:
        print(e)

def purge_db(conn):

    try:
        c = conn.curson()
        c.execute("DELETE FROM tasks where token = *")
        conn.commit()
    except Exception as e:
        print("Failed to purge")
        print(e)

    

    

