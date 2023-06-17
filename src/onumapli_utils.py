import re

def groupcode_organize (text):
    #2 이상의 스페이스 처리
    organized_text = re.sub(' +', ' ',text)

    #컴마를 스페이스로 처리
    organized_text = organized_text.replace(',', ' ')

    #탭을 스페이스로 처리
    organized_text = organized_text.replace('\t', ' ')

    #엔터를 스페이스로 처리
    organized_text = organized_text.replace('\n', ' ')

    return organized_text
