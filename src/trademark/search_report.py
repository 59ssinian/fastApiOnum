from src import notion_custom
from src.trademark import trademark_functions

database_id = '1e60aa4795284be69ccf526819d01767'

def search_report(marks, groups):


    # 로그인 시작
    driver = trademark_functions.login_intomark()
    print("로그인 성공")

    print("메인 검색 진행")
    # 검색 메인 진행
    for mark in marks:
        mark_kor = mark['mark_kor']
        mark_eng = mark['mark_eng']

        section_marks = [mark_kor]

        if mark_eng:
            section_marks.append(mark_eng)
            title = mark_kor + "( " + mark_eng + ")"
        else:
            title = mark_kor

        '''
        (1) 노션 페이지 생성
        '''
        id_page = notion_custom.notion_page_create(database_id, title, "")


        #노션페이지 제1 파트 생성
        '''
        제1 파트
        '''

        first_id_page = "9c51c242c84846cb93d491b3c826415a"
        id_page = notion_custom.notion_page_append_page(id_page, first_id_page)

        #분석대상
        id_page = notion_custom.notion_block_append_semi_title(id_page, "1.1. 상표명")
        id_page = notion_custom.notion_block_append_paragraph(id_page, title)

        id_page = notion_custom.notion_block_append_semi_title(id_page, "1.2. 지정상품")

        i=1
        for group in groups:
            class_no = group['class_no']
            group_code = group['group_code']
            name = group['name']

            search_target = "("+str(i)+") "+"제"+str(class_no)+"류 (유사군:"+group_code+") : "+name+" / 검토결과등급 :"
            id_page = notion_custom.notion_block_append_paragraph(id_page, search_target)
            i=i+1

        first2_id_page = "f206d32e5b4e479c8962255d32454519"
        id_page = notion_custom.notion_page_append_page(id_page, first2_id_page)

        for section_mark in section_marks:

            id_page = notion_custom.notion_block_append_semi_title(id_page, section_mark)

            i=1
            for group in groups:
                class_no = group['class_no']
                group_code = group['group_code']
                name = group['name']

                section = "(" + str(i) + ") " + section_mark + ":" + str(class_no) + "류 / 유사군코드 : " + group_code + " / 지정상품 : " + name

                notion_custom.notion_block_append_paragraph(id_page, section)

                if ( (section_mark.find("%") == -1) and (section_mark.find("/") == -1) ):
                    driver = trademark_functions.search_word_similar(driver, section_mark, class_no, group_code)
                else:
                    driver = trademark_functions.search_word_identical(driver, section_mark, class_no, group_code)

                similar_count = trademark_functions.results_count(driver)['active']
                similar_trademarks = None
                print(similar_count)

                if not similar_count == 0:
                    if similar_count < 10:
                        count = similar_count
                    else:
                        count = 10

                    similar_trademarks_image = trademark_functions.get_trademarks_image(driver, count)
                    similar_trademarks_detail = trademark_functions.get_trademarks_detail(driver, count)

                    trademarks = trademark_functions.merge_trademarks(similar_trademarks_detail, similar_trademarks_image)

                    print("노션기록시작")
                    notion_custom.notion_block_append_trademarks_list(id_page, trademarks)
                    print("노션기록완료")
                else:
                    notion_custom.notion_block_append_trademarks_list_noresult(id_page, "결과 없음")

                i = i + 1

        second_id_page = "ca71d7fff8d44d07a969c66bb91383ca"
        id_page = notion_custom.notion_page_append_page(id_page, second_id_page)

        id_page = notion_custom.notion_block_append_semi_title(id_page, section_mark)

        #google_url = functions.google_search(section_mark)
        #print(google_url)
        #notion_custom.notion_block_append_image(id_page, google_url)

        #naver_url = functions.naver_search(section_mark)
        #notion_custom.notion_block_append_image(id_page, naver_url)


        third_id_page = "b6a0d6cdbb70479c93fbebc5b9d349b5"
        id_page = notion_custom.notion_page_append_page(id_page, third_id_page)


    trademark_functions.logout_intomark(driver)

    return