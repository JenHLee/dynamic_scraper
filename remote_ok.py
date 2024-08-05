import requests
from bs4 import BeautifulSoup
import csv

jobs_db=[]

keywords = ["flutter", "python", "golang"]

def scrape_page(url, headers):
  print(f"Scraping page {url}...")
  response = requests.get(url, headers=headers)

  soup = BeautifulSoup(response.content, "html.parser")

  jobs = soup.find("table", id="jobsboard").find_all("td", class_="company position company_and_position")

  for job in jobs:
    try:
      title = job.find("h2", itemprop="title").text
      company_name = job.find("h3", itemprop="name").text
      location = job.find("div", class_="location").text
      salary = job.find("div", class_="location tooltip").text
      url = job.find("a", itemprop="url")["href"]

      job.data = {
        "title": title,
        "company_name": company_name,
        "location": location,
        "salary" : salary,
        "url": f"https://remoteok.com{url}"
      }

      jobs_db.append(job.data)
    except AttributeError:
     pass

for key in keywords:
  url = f"https://remoteok.com/remote-{key}-jobs"    
  headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}
  scrape_page(url, headers)

# Create CSV file    
file = open("jobs_remote_ok.csv", "w")
writer = csv.writer(file)

# Header
writer.writerow(["Title", "Company", "Location", "Salary", "URL"])

# Data - only values as a list
for job in jobs_db:
    writer.writerow(job.values())
file.close()







