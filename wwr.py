import requests
from bs4 import BeautifulSoup
import csv

jobs_db = []

def scrape_page(url):
  print(f"Scrapping {url}...")
  response = requests.get(url)

  soup = BeautifulSoup(response.content, "html.parser")

  jobs = soup.find("section", class_="jobs").find_all("li")[1:-1]

  for job in jobs:
    title = job.find("span", class_="title").text
    companies = job.find_all("span", class_="company")
    url = job.find("div", class_="tooltip--flag-logo").next_sibling["href"]
    if len(companies) == 3:
      company, position, region = companies
      company = company.text
      position = position.text
      region = region.text

      job_data = {
          "title": title,
          "company": company,
          "position": position,
          "region": region,
          "url": f"https://weworkremotely.com{url}"
      }
      jobs_db.append(job_data)

def get_pages(url):
  response = requests.get(url)
  soup = BeautifulSoup(response.content, "html.parser")
  return len(
    soup.find("div", class_="pagination").find_all("span", class_="page"))

total_pages = get_pages("https://weworkremotely.com/top-trending-remote-jobs?page=1")

for x in range(total_pages):
  url = f"https://weworkremotely.com/top-trending-remote-jobs?page={x+1}"
  scrape_page(url)

# Create CSV file
file = open("jobs_wwr.csv", "w")
writer = csv.writer(file)

# Header
writer.writerow(["Title", "Company", "Position", "Region", "URL"])

# Data - only values as a list
for job in jobs_db:
    writer.writerow(job.values())
file.close()



