from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import re

def get_groupcode(search_expression):

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(database="onumaplidb", user="postgres", password="100million1@", host="localhost", port="5432")
    cur = conn.cursor()

    modified_query=modify_search_query(search_expression)

    # Build the SQL query
    query = "SELECT name_kor FROM groupcodes_main WHERE " + modified_query


    # Execute the SQL query
    cur.execute(query)

    # Fetch the results
    rows = cur.fetchall()

    print(rows)

    result = [row[0] for row in rows]
    print(result)
    cur.close()
    conn.close()

    return result


def modify_search_query(text):

    # 컴마 이후 공백 정리
    text=re.sub(r',\s+', ',',text)

    query_items=text.split(',')

    modify_query=""

    for index, item in enumerate(query_items):

        item_query = ""

        if item[0] !='(':
            item_query = " name_kor LIKE '%"+item+"%' "
        else:
            item_query=item.replace("(", "(name_kor LIKE '%") \
                .replace(" and ", "%' and name_kor LIKE '%") \
                .replace("and", "%' and name_kor LIKE '%") \
                .replace(" & ", "%' and name_kor LIKE '%") \
                .replace("&", "%' and name_kor LIKE '%") \
                .replace(")", "%')")

        modify_query=modify_query+item_query

        if index + 1 < len(query_items):
            modify_query = modify_query + " or "

    return modify_query
