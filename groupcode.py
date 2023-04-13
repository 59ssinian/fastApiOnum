from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import re

def get_connection():

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(database="onumaplidb", user="postgres", password="100million1@", host="localhost",
                            port="5432")

    return conn

def get_groupcode(search_expression):

    # Connect to the PostgreSQL database
    conn = get_connection()
    cur = conn.cursor()

    modified_query=modify_search_query(search_expression)

    # Build the SQL query
    query = "SELECT DISTINCT groupcode FROM groupcodes_main WHERE " + modified_query


    # Execute the SQL query
    cur.execute(query)

    # Fetch the results
    rows = cur.fetchall()

    result = [row[0] for row in rows]
    cur.close()
    conn.close()

    return result

def get_items_by_groupcode(groupcodes):

    # Connect to the PostgreSQL database
    conn = get_connection()
    cur = conn.cursor()

    items_group=[]

    for groupcode in groupcodes:

        modified_query = "groupcode = '"+groupcode+"' "
        order_query = " ORDER BY niceclass ASC"

        # Build the SQL query
        query = "SELECT DISTINCT niceclass FROM groupcodes_main WHERE " \
                +modified_query + order_query

        cur.execute(query)
        rows = cur.fetchall()
        niceclasses = [row[0] for row in rows]

        for index, niceclass in niceclasses:

            # 대표명칭 찾기
            modified_query = "groupcode = '" + groupcode \
                             + "' and niceclass = "+ str(niceclass) \
                             + " and represent = true "

            order_query = " ORDER BY niceclass ASC"

            query = "SELECT DISTINCT name_kor FROM groupcodes_main WHERE " \
                    + modified_query + order_query

            cur.execute(query)
            rows = cur.fetchall()
            represents = [row[0] for row in rows]

            # 대표명칭 합하기
            represent_names=""

            for represent in represents:
                represent_names=represent_names+represent

                if index + 1 < len(niceclasses):
                    represent_names = represent_names + ", "


            #전체 명칭 찾기
            modified_query = "groupcode = '" + groupcode \
                             + "' and niceclass = " + niceclass

            order_query = ""

            query = "SELECT DISTINCT name_kor FROM groupcodes_main WHERE " \
                    + modified_query + order_query

            cur.execute(query)
            rows = cur.fetchall()
            names = [row[0] for row in rows]

            #전체명칭 합하기
            names_sum = ""

            for name in names:
                names_sum = names_sum + name

                if index + 1 < len(names):
                    names_sum = names_sum + ", "

            items_group.append(
                {'groupcode': groupcode,
                 'niceclass': niceclass,
                 'represent': represent_names,
                 'names': names_sum})
    cur.close()
    conn.close()

    return items_group



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
