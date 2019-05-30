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
        return conn
    except Exception as e:
        print(e)

def insert_task(conn, token, dic, date_str):

    insert_token_sql = \
    """
<<<<<<< HEAD
        INSERT INTO tasks(token, json) VALUES(?,?,?);
=======
        INSERT INTO tasks(token, json, start_date) VALUES(?,?,?);
>>>>>>> d660886a6457e560a2a7be218a381e91613b0b00
    """
   
    try:
        dic['date'] = dic['date'].strftime('%Y-%m-%d %H:%M:%S')
        vals = (token, json.dumps(dic), date_str)
        c = conn.cursor()
        c.execute(insert_token_sql, vals)
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
        c.execute(retrieve_token_sql, (token, ))
        rows = c.fetchall()
        print(len(rows))
        return {rows[0][1]:json.loads(rows[0][2])}

    except Exception as e:
        print(e)

    

    

