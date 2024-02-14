import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
pw = os.environ.get("DB")

# CREATE TABLE test (
#     id SERIAL PRIMARY KEY,
#     name VARCHAR(255)
# );

def create_connection(pw):
    conn = psycopg2.connect(
        host="localhost", database="sql_injection", user="postgres", password=pw)
    return conn

def add_record_vulnerable(con, name):
    # INSERT INTO test (name) VALUES (''); DROP TABLE test; --')
    query = f"INSERT INTO test (name) VALUES ('{name}')"
    with con:
        with con.cursor() as cursor:
            cursor.execute(query)
            con.commit()

con = create_connection(pw=pw)

name = "'); DROP TABLE test; --"
# The "'); tries to finish the VALUES-section in order to start a new query
# The -- is added to remove any further SQL-statements that might interfere
add_record_vulnerable(con, name)

con.close()