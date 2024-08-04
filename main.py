from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
p = sync_playwright().start()

browser = p.chromium.launch(headless=False)

page = browser.new_page()

page.goto("https://www.wanted.co.kr/jobsfeed")
time.sleep(5)

page.click("button.Aside_searchButton__rajGo")
time.sleep(5)

page.get_by_placeholder("검색어를 입력해 주세요.").fill("flutter")
time.sleep(5)

page.keyboard.down("Enter")
time.sleep(5)

page.click("a#search_tab_position")
time.sleep(5)

for x in range(5):
    time.sleep(5)
    page.keyboard.down("End")

content = page.content()

p.stop()

soup = BeautifulSoup(content, "html.parser")
print(soup)