from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2

def get_groupcode(search_expression):

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(database="onumaplidb", user="onumapli", password="100million1@", host="localhost", port="5432")
    cur = conn.cursor()

    # Build the SQL query
    query = "SELECT * FROM groupcodes WHERE " + search_expression.replace("AND", "AND name_kor LIKE").replace("OR", "OR name_kor LIKE").replace("(", "(name_kor LIKE '%").replace(")", "%')")

    # Execute the SQL query
    cur.execute(query)

    # Fetch the results
    rows = cur.fetchall()

    for row in rows:
        print(row)

    result = [row[0] for row in rows]
    cur.close()
    conn.close()

    return result