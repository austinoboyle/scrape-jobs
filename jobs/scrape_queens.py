from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import json
import os


def queens():
    # Get URL, use to get info
    QUEENS_CAREERS_URL = 'https://queensu.njoyn.com/cl4/xweb/Xweb.asp?tbtoken=Zl5aRR8XCB1xEHQDN1AmCCM%2FBmdEcCJfBkgjWiwME2UtXEQSXUdpcWMuJS5ALiRedQkbUxFaS3cqWA%3D%3D&chk=dFlbQBJe&page=joblisting&CLID=74827'
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(QUEENS_CAREERS_URL)

    scraped_jobs = []
    col_titles = ['id', 'title', 'category', 'type', 'openDate', 'closeDate']

    table = driver.find_element_by_id('searchtable')
    jobs = table.find_elements_by_css_selector('tbody tr')

    # Add to job dictionary
    for job in jobs:
        job_dict = {}
        cols = job.find_elements_by_tag_name('td')
        link = job.find_element_by_css_selector(
            'a[title="View job details"]').get_attribute('href')
        job_dict['url'] = link
        job_dict['img'] = "http://www.queensu.ca/mc_administrator/sites/default/files/assets/pages/QueensLogo_colour.jpg"
        job_dict['company'] = "Queen's University"
        for title, col in zip(col_titles, cols):
            job_dict[title] = col.text

        # Go to page to get description
        page = requests.get(link)
        soup = BeautifulSoup(page.text, 'html.parser')
        desc = soup.find_all(class_="njnSection noborder")[1].text
        job_dict['description'] = desc

        # Append job to positions array
        scraped_jobs.append(job_dict)

    # Dump positions to json
    with open('../json_files/queens_jobs.json', 'w') as out:
        json.dump(scraped_jobs, out)
