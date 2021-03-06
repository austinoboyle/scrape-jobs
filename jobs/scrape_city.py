from selenium import webdriver
import json
from pprint import pprint
import requests
from bs4 import BeautifulSoup


def city():
    # Get URL, use to get info
    CITY_CAREERS_URL = 'https://careers.cityofkingston.ca/CL2/xweb/XWeb.asp?tbtoken=YF9bQhwXCGh2Yy4lLkAuJF5wNlQmCFY%2FBhdEcCIocEggISx%2BExVQKjIdUUQfBWEEAwkbUhRXTncqWA%3D%3D&chk=dFlbQBJe&clid=61577&Page=joblisting&CategoryID=2325,2326,2327,2328,2329,2330,2331,2332,2333,2334,2335,2336,2337,2338,2339,2340,2341,2342,2343,2344,2345,2346,2347,2348,2349,2350,2351,2352,2354,2355,2356,2357'
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(CITY_CAREERS_URL)
    scraped_jobs = []

    # Get table and jobs in table
    table = driver.find_element_by_id('searchtable')
    jobs = table.find_elements_by_css_selector('tbody tr')

    # Add to job dictionary
    for job in jobs:
        job_dict = {}
        cols = job.find_elements_by_tag_name('td')
        link = job.find_element_by_css_selector(
            'a[title="View job details"]').get_attribute('href')
        job_dict['url'] = link
        job_dict['img'] = 'https://www.cityofkingston.ca/image/layout_set_logo?img_id=10672&t=1525661847229'
        job_dict['company'] = 'City of Kingston'
        # Get more information from the job url
        job_page = requests.get(link)
        job_soup = BeautifulSoup(job_page.text, 'html.parser')
        job_dict['description'] = job_soup.find("div", {"id": "jobDetailInformation"}).text.strip()
        job_dict['title'] = job_soup.find(class_="longitem").text.strip()

        # Append job to positions array
        scraped_jobs.append(job_dict)

    # Dump positions to json
    with open('../json_files/city_jobs.json', 'w') as out:
        json.dump(scraped_jobs, out)
