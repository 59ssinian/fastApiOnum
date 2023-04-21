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


def get_groupcode_by_niceclass(niceclass):

    # Connect to the PostgreSQL database
    conn = get_connection()
    cur = conn.cursor()

    modified_query="niceclass="+str(niceclass)+";"

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

    items_groups=[]


    for groupcode in groupcodes:

        #먼저 groupcode 입력
        items_group = {}
        items_group['groupcode']=groupcode

        #front에서 사용할 변수 생성 : showContent
        items_group['showContent'] = True
        items_group['classgroup'] = []

        modified_query = "groupcode = '"+groupcode+"' "
        order_query = " ORDER BY niceclass ASC"

        # Build the SQL query
        query = "SELECT DISTINCT niceclass FROM groupcodes_main WHERE " \
                +modified_query + order_query

        cur.execute(query)
        rows = cur.fetchall()
        #print(rows)
        niceclasses = [row[0] for row in rows]

        #print(niceclasses)

        for niceclass in enumerate(niceclasses):
            #print("niceclass:"+str(niceclass[1]))
            # 대표명칭 찾기
            modified_query = "groupcode = '" + groupcode \
                             + "' and niceclass = "+ str(niceclass[1]) \
                             + " and represent = true "

            order_query = ""

            query = "SELECT DISTINCT name_kor FROM groupcodes_main WHERE " \
                    + modified_query + order_query

            cur.execute(query)
            rows = cur.fetchall()
            represents = [row[0] for row in rows]

            # 대표명칭 합하기
            #represent_names=sum_items(represents)


            #전체 명칭 찾기
            modified_query = "groupcode = '" + groupcode \
                             + "' and niceclass = " + str(niceclass[1])

            order_query = "ORDER BY sourcescount DESC"

            query = "SELECT DISTINCT name_kor, sourcescount, groupcode, niceclass FROM groupcodes_main WHERE " \
                    + modified_query + order_query

            cur.execute(query)
            rows = cur.fetchall()
            #names = [row[0] for row in rows], [row[1] for row in rows]
            names = [{'name':row[0], 'counts':row[1], 'groupcode':row[2], 'niceclass':row[3]} for row in rows]

            #전체명칭 합하기
            #names_sum = sum_items(names)

            items_group['classgroup'].append(
                {'niceclass':niceclass, 'represent':represents, 'names':names}
            )

        items_groups.append(items_group)

    cur.close()
    conn.close()

    return items_groups

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
                .replace(" & ", "%' and name_kor LIKE '%") \
                .replace("&", "%' and name_kor LIKE '%") \
                .replace(")", "%')")

        modify_query=modify_query+item_query

        if index + 1 < len(query_items):
            modify_query = modify_query + " or "

    return modify_query

def sum_items(items):
    sum_text=""
    #print(items)
    #print("아이템 수:")
    #print(len(items))

    index=0
    for item in items:
        #print(item)
        sum_text = sum_text + item

        if index + 1 < len(items):
            sum_text = sum_text + ", "

        index+=1

    return sum_text
