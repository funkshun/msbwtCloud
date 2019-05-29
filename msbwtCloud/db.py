import sqlite3
import json
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
        INSERT INTO tasks(token, json) VALUES(?,?);
    """
   
    try:
        vals = (token, json.dumps(dic), date_str)
        c = conn.cursor()
        c.execute(insert_token_sql, vals)
        return c.lastrowid

def retrieve_token(conn, token):

    retrieve_token_sql = \
        """
            SELECT * FROM tasks WHERE token = ?;
        """

    try:
        c = conn.cursor()
        c.execute(retrieve_token_sql, (token, ))
        rows = c.fetchall()

        return {rows[0][1]:json.loads(rows[0][2])}
    except Exception as e:
        print(e)

    

    

