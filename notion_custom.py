from notion_client import Client
from pprint import pprint
from datetime import date



private_key = "secret_BagWaishDYjawGs7XKPpGWXqRwHSeIDruQ7gnV2BRoq"
notion = Client(auth=private_key)

def notion_page_create(database_id, title, first_paragraph):

    today = date.today()
    date_string = today.strftime("%Y-%m-%d")

    new_page = {
        "이름": {"title": [{"text": {"content": title}}]},
        "작성일" : {"date": { "start":date_string}}
    }

    new_children = [{
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {
                        "content": first_paragraph}}]
                }
            }]

    created_page = notion.pages.create(parent={"database_id": database_id}, properties=new_page, children=new_children)

    id_created_page=created_page['id']


    return id_created_page

def notion_block_append_semi_title(id_page, semi_title):

    notion = Client(auth=private_key)

    new_block = [{
        "object": "block",
        "type": "heading_3",
        "heading_3": {

            "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": semi_title
                    }
                 }],
                "color": "default"
        }
    }]

    created_block = notion.blocks.children.append(block_id=id_page, children=new_block)

    return id_page

def notion_block_append_paragraph(id_page, paragraph):

    notion = Client(auth=private_key)

    new_block = [{
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": paragraph
                    }
                 }
            ]
        }
    }]

    created_block = notion.blocks.children.append(block_id=id_page, children=new_block)

    return id_page

def notion_block_append_bulletlist(id_page, item):

    notion = Client(auth=private_key)

    new_block = [{
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": item
                    }
                 }
            ]
        }
    }]

    created_block = notion.blocks.children.append(block_id=id_page, children=new_block)

    return id_page

def notion_block_append_image(id_page, url):

    notion = Client(auth=private_key)

    new_block = [{
        "object": "block",
        "type": "image",
        "image": {
            "type": "external",
            "external": {
                "url": url
            }
        }
    }]

    created_block = notion.blocks.children.append(block_id=id_page, children=new_block)

    return id_page

def notion_block_append_trademarks(id_page, trademarks):

    notion = Client(auth=private_key)

    for trademark in trademarks:
        status = trademark['status']
        number = trademark['number']
        url = trademark['url']

        notion_block_append_image(id_page, url)
        notion_block_append_paragraph(id_page, status+number)

    return

def notion_block_append_trademarks_list(id_page, trademarks_detail):

    notion = Client(auth=private_key)

    # 나중에 이미지 링크를 넣어야 함


    for trademark in trademarks_detail:

        text = "["+trademark['status']+"] "+trademark['mark']
        url = trademark['url']

        if trademark['reg_number']:
            text = text + " ("+ trademark['reg_number']+"("+trademark['app_date']+")) / "+trademark['applicant']
        else:
            if not trademark['app_number']:
                text = text + " (" + "국제출원" + ")) / " + trademark['applicant']
            else:
                text = text + " (" + trademark['app_number'] + "(" + trademark['app_date'] + ")) / " + trademark[
                'applicant']



        notion_block_append_bulletlist(id_page, text)

    return

def notion_block_append_trademarks_list_noresult(id_page, text):

    notion_block_append_bulletlist(id_page, text)

    return


def notion_page_append_page(id_page, source_id_page):

    page =notion.blocks.children.list(source_id_page)
    results=page['results']

    for result in results:

        block = notion.blocks.children.append(block_id=id_page, children=[result])
        block_id=block['results'][0]['id']

        if (result['has_children'] == True):
            sub_page = notion.blocks.children.list(result['id'])
            sub_results=sub_page['results']

            notion.blocks.children.append(block_id=block_id, children=sub_results)

    return id_page





