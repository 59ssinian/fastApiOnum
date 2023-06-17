import src.notion_custom as notion_custom
import src.trademark.trademark_functions as functions

database_id = 'c985b36c8cec439182cc0e322c863478'

def mass_report(marks, groups):

    mark_title = marks[0]['mark_kor']

    # 노션페이지 생성해야함
    '''
    (1) 노션 페이지 생성
    '''
    id_page = notion_custom.notion_page_create(database_id, mark_title, "")


    # 로그인 시작
    driver = functions.login_intomark()

    # 검색 메인 진행
    for mark in marks:
        mark_kor = mark['mark_kor']
        mark_eng = mark['mark_eng']

        marks = [mark_kor]

        if mark_eng:
            marks.append(mark_eng)
            title = mark_kor + "( " + mark_eng + ")"
        else:
            title = mark_kor

        # 노션페이지 항목 생성
        '''
        (2) 항목 생성
        ### "A" 상표 검색
        '''

        notion_custom.notion_block_append_semi_title(id_page, title)

        for mark in marks:

            i = 1
            for group in groups:
                class_no =group['class_no']
                group_code =group['group_code']
                name = group['name']

                search_target = "("+str(i)+") "+"제"+str(class_no)+"류 (유사군:"+group_code+") : "+name+" / 검토결과등급 :"

                notion_custom.notion_block_append_paragraph(id_page, search_target)
                i=i+1

                # 일치검색을 한 후, 발견되면 이를 기재하고, 유사검색을 실시한다.
                '''
                result_driver = functions.search_word_identical(driver, mark_kor, class_no, group_code)
                identical_count = functions.results_count(result_driver)
                identical_trademarks = None
                if not identical_count==0:
                    identical_trademarks = functions.get_trademarks(result_driver)
                '''

                # 유사검색
                driver = functions.search_word_similar(driver, mark, class_no, group_code)
                similar_count = functions.results_count(driver)['active']
                similar_trademarks = None
                print(similar_count)

                if not similar_count == 0:
                    if similar_count <10:
                        count = similar_count
                    else:
                        count = 10

                    similar_trademarks_image = functions.get_trademarks_image(driver, count)
                    similar_trademarks_detail = functions.get_trademarks_detail(driver, count)

                    trademarks = functions.merge_trademarks(similar_trademarks_detail, similar_trademarks_image)


                    print("노션기록시작")
                    notion_custom.notion_block_append_trademarks_list(id_page, trademarks)
                    print("노션기록완료")
                else:
                    notion_custom.notion_block_append_trademarks_list_noresult(id_page, "결과 없음")


    functions.logout_intomark(driver)

    return