from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import re

#로그인파트(driver)
def login_intomark():

    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--headless')
    
    #로그인 파트 시작
    print("login_start")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.intomark.com/service/mai/main.wips")

    # Set the window size to 800 pixels wide and 600 pixels high
    driver.set_window_size(1100, 800)

    input_field = driver.find_element("id", "username")
    input_field.send_keys("omipc2")

    input_field = driver.find_element("id", "password")
    input_field.send_keys("omipc2.com")

    link = driver.find_element("link text", "로그인")
    link.click()

    try:
        alert = driver.switch_to.alert
        alert.accept()
        print("pop up is clear")
    except Exception:
        print("no pop up")


    print("login_complete")

    return driver

#로그아웃(driver)
def logout_intomark(driver):

    link = driver.find_element("xpath", "//span[contains(.,'로그아웃')]")
    link.click()

    print("logoout_complete")
    return driver

#유사검색(result_driver)
def search_word_similar(driver, mark1, class1, group1):

    #유사검색시작
    print(mark1+", "+str(class1)+", "+group1+": 유사검색시작")

    link = driver.find_element("link text", "국가별검색")
    link.click()

    wait = WebDriverWait(driver, 10)
    xpath = "//li[2]/button"
    wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

    #유사검색
    link = driver.find_element("xpath", "//li[2]/button")
    link.click()

    input_field = driver.find_element("id", "tmarkNmArea")
    input_field.send_keys(mark1)

    input_field = driver.find_element("id", "smlrCdArea")
    input_field.send_keys(group1)

    link = driver.find_element("xpath", "//div[2]/a/span")
    link.click()

    wait = WebDriverWait(driver, 10)
    xpath = "//article/div/div/div/span"
    wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

    #유사검색완료
    print(mark1+", "+str(class1)+", "+group1+": 검색완료")

    result_driver = driver

    return result_driver

#일치검색(result_driver)
def search_word_identical(driver, mark1, class1, group1):

    # 일치검색시작
    print(mark1 + str(class1) + group1 + ": 일치검색시작")

    link = driver.find_element("link text", "국가별검색")
    link.click()

    # 일반검색
    link = driver.find_element("xpath", "//li/button")
    link.click()

    input_field = driver.find_element("id", "tmarkNmArea")
    input_field.send_keys(mark1)

    input_field = driver.find_element("id", "smlrCdArea")
    input_field.send_keys(group1)

    link = driver.find_element("xpath", "//div[2]/a/span")
    link.click()

    wait = WebDriverWait(driver, 10)
    xpath = "//article/div/div/div/span"
    wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

    #일치검색완료
    print(mark1+str(class1)+group1+": 검색완료")

    result_driver = driver

    return result_driver

#검색카운트(numbers)
def results_count(result_driver):

    print("count 획득 설정")

    wait = WebDriverWait(result_driver, 10)
    xpath = "//article/div/div/div/span"
    wait.until(EC.text_to_be_present_in_element((By.XPATH, xpath),"총"))

    xpaths = []
    xpaths.append({"name": "total", "xpath":"//article/div/div/div/span"})
    xpaths.append({"name": "filing", "xpath": "//li/ul/li/a"})
    xpaths.append({"name": "pub", "xpath": "//li/ul/li[2]/a"})
    xpaths.append({"name": "reg", "xpath": "//li/ul/li[3]/a"})
    xpaths.append({"name": "reject", "xpath": "//li[2]/ul/li/a"})
    xpaths.append({"name": "expired", "xpath": "//li[2]/ul/li[2]/a"})
    xpaths.append({"name": "cancel", "xpath": "//li[2]/ul/li[3]/a"})
    xpaths.append({"name": "abandon", "xpath": "//li[2]/ul/li[4]/a"})
    xpaths.append({"name": "invalid", "xpath": "//li[2]/ul/li[5]/a"})

    numbers={}

    # fine element by id
    for xpath in xpaths:

        try:
            element = result_driver.find_element("xpath", xpath['xpath'])

            if element.is_displayed():
                number = int(re.findall(r'\d+', element.text)[0])
            else:
                number = 0
        except Exception:
            number = 0

        numbers.update({xpath['name']:number})

    print(numbers)

    print("count 수집 완료")

    active = numbers['filing']+numbers['pub']+numbers['reg']

    numbers = {"active" : active }

    print("active : "+str(active))

    return numbers

#뷰의 조정(1, 2, 3)
def change_view(result_driver, number):

    print("view change")
    view_xpath = ["//article[2]/div/ul/li/a",
                  "//article[2]/div/ul/li[2]/a",
                  "//article[2]/div/ul/li[3]/a"]

    # view setting
    link = result_driver.find_element("xpath", view_xpath[number])
    link.click()

    try:
        # wating to view setting
        wait = WebDriverWait(result_driver, 3)
        xpath = "//body/div[2]/p"
        wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

        wait = WebDriverWait(result_driver, 3)
        wait.until_not(EC.presence_of_element_located((By.XPATH, xpath)))

    except Exception:
        print("로딩 지연 없음")

    print("view changed")


def get_trademarks_group_image(result_driver, filename):
    print("group image start")

    # 뷰 조정
    change_view(result_driver,2)

    # Locate the element that you want to capture
    element = result_driver.find_element("xpath", "//div[4]/ul")

    # Use the get_screenshot_as_file() method to capture a screenshot of the element
    url = "snapshot/"+filename+".png"
    element.screenshot(url)

    return url



#상표정보획득_이미지
def get_trademarks_image(result_driver, count):
    print("trademark start")

    trademarks_image = []

    # 뷰 조정
    change_view(result_driver,2)

    try :
        status_element = result_driver.find_element("xpath", "//span/span/span")
        app_number_element = result_driver.find_element("xpath", "//label/span/a")
        url_element = result_driver.find_element("xpath", "//td/img")
    except Exception:
        return trademarks_image

    if status_element:
        status = status_element.text
        app_number = app_number_element.text
        url = url_element.get_attribute('src')

        trademarks_image.append({"status" : status, "number" : app_number, "url" : url})
    else:
        return trademarks_image

    for i in range(2,count):

        status_xpath = "//li["+str(i)+"]/div/div[3]/span/span/span"
        app_number_xpath = "//li["+str(i)+"]/div/div[3]/label/span/a"
        url_xpath = "//li["+str(i)+"]/div/div/ul/li/table/tbody/tr/td/img"

        try:
            status_element = result_driver.find_element("xpath", status_xpath)
            app_number_element = result_driver.find_element("xpath", app_number_xpath)
            url_element = result_driver.find_element("xpath", url_xpath)

            status = status_element.text
            app_number = app_number_element.text
            url = url_element.get_attribute('src')

            trademarks_image.append({"status": status, "number": app_number, "url": url})

        except Exception:
            status_element = None

    print(trademarks_image)

    return trademarks_image


# 상표정보획득_상세
def get_trademarks_detail(result_driver, count):
    print("trademark start")

    trademarks_detail = []

    # 뷰 조정
    change_view(result_driver, 0)

    try :
        status_element = result_driver.find_element("xpath", "//td[3]/span")
    except Exception:
        return trademarks_detail


    if status_element:
        status = status_element.text
        classno = result_driver.find_element("xpath", "//div[2]/div/table/tbody/tr/td[4]").text
        mark=result_driver.find_element("xpath", "//td[8]/a").text
        applicant=result_driver.find_element("xpath", "//div[2]/div/table/tbody/tr/td[9]").text

        try:
            app_number = result_driver.find_element("xpath", "//td[5]/a").text
        except Exception:
            app_number = None

        try:
            reg_number = result_driver.find_element("xpath", "//td[7]/a").text
        except Exception:
            reg_number = None

        try:
            owner=result_driver.find_element("xpath", "//div[2]/div/table/tbody/tr/td[10]").text
        except Exception:
            owner = None

        try:
            app_date = result_driver.find_element("xpath", "//div[2]/div/table/tbody/tr/td[6]").text
        except Exception:
            app_date = None







        trademarks_detail.append({"status": status,
                                  "classno": classno,
                                  "app_number": app_number,
                                  "app_date": app_date,
                                  "reg_number": reg_number,
                                  "mark": mark,
                                  "applicant": applicant,
                                  "owner": owner})

    else:
        return trademarks_detail

    for i in range(2, count):

        status_xpath="//tr["+str(i)+"]/td[3]/span"
        classno_xpath="//div[2]/div/table/tbody/tr["+str(i)+"]/td[4]"
        app_number_xpath="//tr["+str(i)+"]/td[5]/a"
        app_date_xpath="//div[2]/div/table/tbody/tr["+str(i)+"]/td[6]"
        reg_number_xpath="//tr["+str(i)+"]/td[7]/a"
        mark_xpath="//tr["+str(i)+"]/td[8]/a"
        applicant_xpath="//div[2]/div/table/tbody/tr["+str(i)+"]/td[9]"
        owner_xpath="//div[2]/div/table/tbody/tr["+str(i)+"]/td[9]"

        try:
            status = result_driver.find_element("xpath", status_xpath).text
            classno = result_driver.find_element("xpath", classno_xpath).text
            mark = result_driver.find_element("xpath", mark_xpath).text
            applicant = result_driver.find_element("xpath", applicant_xpath).text

            try:
                reg_number = result_driver.find_element("xpath", reg_number_xpath).text
            except Exception:
                reg_number = None

            try:
                owner = result_driver.find_element("xpath", owner_xpath).text
            except Exception:
                owner = None

            try:
                app_number = result_driver.find_element("xpath", app_number_xpath).text
            except Exception:
                app_number = None

            try:
                app_date = result_driver.find_element("xpath", app_date_xpath).text
            except Exception:
                app_date = None

            trademarks_detail.append({"status": status,
                                      "classno": classno,
                                      "app_number": app_number,
                                      "app_date": app_date,
                                      "reg_number": reg_number,
                                      "mark": mark,
                                      "applicant": applicant,
                                      "owner": owner})
        except Exception:
            status=None

    print(trademarks_detail)

    return trademarks_detail


#trademark 정보 병합
def merge_trademarks(trademarks_detail, trademarks_image):

    i=0
    for tradrmark_detail in trademarks_detail:
        tradrmark_detail.update(trademarks_image[i])
        i=i+1

    return trademarks_detail


def naver_search(text):

    naver_driver = webdriver.Chrome()
    naver_driver.get("https://search.naver.com/search.naver?query="+text)

    url = "snapshot/"+text+"_naver.png"

    naver_driver.get_screenshot_as_file(url)

    return url


def google_search(text):
    google_driver = webdriver.Chrome()
    google_driver.get("https://www.google.com/search?q=" + text)

    url = "snapshot/" + text + "_google.png"

    google_driver.get_screenshot_as_file(url)

    return url