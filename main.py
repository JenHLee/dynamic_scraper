from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

p = sync_playwright().start()

browser = p.chromium.launch(headless=False)

page = browser.new_page()

page.goto("https://www.wanted.co.kr/search?query=flutter&tab=position")

#page.goto("https://www.wanted.co.kr/jobsfeed")
# time.sleep(5)

# page.click("button.Aside_searchButton__rajGo")
# time.sleep(5)

# page.get_by_placeholder("검색어를 입력해 주세요.").fill("flutter")
# time.sleep(5)

# page.keyboard.down("Enter")
# time.sleep(5)

# page.click("a#search_tab_position")
# time.sleep(5)

jobs_db = []

for x in range(5):
    time.sleep(5)
    page.keyboard.down("End")

content = page.content()

p.stop()

soup = BeautifulSoup(content, "html.parser")

jobs = soup.find_all("div", class_="JobCard_container__REty8")

for job in jobs:
    link = f"https://www.wanted.co.kr/{job.find('a')['href']}"
    title = job.find("strong", class_="JobCard_title__HBpZf").text
    company_name = job.find("span", class_="JobCard_companyName__N1YrF").text
    reward = job.find("span", class_="JobCard_reward__cNlG5").text
    job = {
        "title": title,
        "company_name" : company_name,
        "reward" : reward,
        "link" : link
    }
    jobs_db.append(job)
    
file = open("jobs.csv", "w")
writer = csv.writer(file)
#header
writer.writerow(["Title", "Company", "Reward", "Link"])

#data - only values as a list
for job in jobs_db:
    writer.writerow(job.values())


