from selenium import webdriver
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


from bs4 import BeautifulSoup
import time
import pandas as pd

url = 'https://www.tripadvisor.co.kr/Restaurant_Review-g294197-d3200324-Reviews-Jungsik-Seoul.html'

service = Service(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service)

browser.implicitly_wait(5)  # 브라우저를 close()할 때까지 적용.
                            # 찾는 element가 생길때까지 최대 5초 대기.

# time.sleep(10)
browser.maximize_window()
#url 페이지로 이동
browser.get(url)

title = []
content = []

while True:
    try:
        time.sleep(2)
        more_btn = browser.find_element(By.CSS_SELECTOR, ".taLnk.ulBlueLinks")
        more_btn.click()

        time.sleep(2)

        html = browser.page_source
        soup = BeautifulSoup(html, "lxml")
        comment_title = soup.select(".noQuotes")
        comment_tag_list = soup.select("p.partial_entry")

        for tag in comment_title:
            title.append(tag.text)   #tag.get_text().strip()

        for tag in comment_tag_list:
            content.append(tag.text)   #tag.get_text().strip()

        # 다음버튼 클릭

        browser.find_element(By.CSS_SELECTOR, 'a.nav.next.ui_button.primary').click()
    except:
        break
        pass
        
browser.close()

df = pd.DataFrame({"title":title, "content":content})

print(df)

df.to_csv("트립어드바이저_댓글크롤링.csv", encoding="EUC-KR")