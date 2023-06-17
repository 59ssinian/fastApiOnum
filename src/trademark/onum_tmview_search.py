#selenium을 이용하여 https://www.tmdn.org/tmview/#/tmview 사이트에 접속하여, 검색어를 입력하고 결과를 스크랩하는 코드
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import re
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

#사이트 접속
def site_connect():
	
	site_url = "https://www.tmdn.org/tmview/"
	
	
	print("접속시작")
	
	chrome_options = Options()
	chrome_options.add_argument('--ignore-certificate-errors')
	chrome_options.add_argument('--headless')
	
	# Adding argument to disable the AutomationControlled flag
	chrome_options.add_argument("--disable-blink-features=AutomationControlled")
	
	# Exclude the collection of enable-automation switches
	chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
	
	# Turn-off userAutomationExtension
	chrome_options.add_experimental_option("useAutomationExtension", False)
	
	driver = webdriver.Chrome(options=chrome_options)
	
	# Changing the property of the navigator value for webdriver to undefined
	driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
	
	driver.get(site_url)

	# Set the window size to wide and high
	#driver.set_window_size(1100, 800)
	
	# Wait for the page to load
	#wait = WebDriverWait(driver, 1)
	#xpath = "//input"
	#wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
	
	print("접속완료")
	
	return driver

#검색어 입력
def search_word(driver, word, country, classes):
	
	# 고급검색 확장
	return

	
	



