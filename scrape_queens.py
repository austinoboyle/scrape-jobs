from selenium import webdriver
import json
from pprint import pprint
import os


def queens():
    # Get URL, use to get info
    QUEENS_CAREERS_URL = 'https://queensu.njoyn.com/cl4/xweb/Xweb.asp?tbtoken=Zl5aRR8XCB1xEHQDN1AmCCM%2FBmdEcCJfBkgjWiwME2UtXEQSXUdpcWMuJS5ALiRedQkbUxFaS3cqWA%3D%3D&chk=dFlbQBJe&page=joblisting&CLID=74827'
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(QUEENS_CAREERS_URL)

    with open('sectors.json') as data_file:
        data = json.load(data_file)
    sectors = []
    for header in data:
        sectors.append(header)

    scraped_jobs = []
    #NUM_COLS = 6
    col_titles = ['ID', 'Title', 'Category', 'Type', 'Open_Date', 'Close_Date']

    table = driver.find_element_by_id('searchtable')
    jobs = table.find_elements_by_css_selector('tbody tr')

    # Add to job dictionary
    for job in jobs:
        job_dict = {}
        cols = job.find_elements_by_tag_name('td')
        link = job.find_element_by_css_selector(
            'a[title="View job details"]').get_attribute('href')
        job_dict['URL'] = link
        job_dict['Company'] = "Queen's University"
        for title, col in zip(col_titles, cols):
            job_dict[title] = col.text
        job_dict['Sectors'] = []

        # Determine sectors of job
        for sector in sectors:
            for syn in data[sector]:
                if(syn.lower() in job_dict['Title'].lower()):
                    job_dict['Sectors'].append(sector)
                    break

        # Append job to positions array
        scraped_jobs.append(job_dict)

    # Dump positions to json
    with open('./json_files/queens_jobs.json', 'w') as out:
        json.dump(scraped_jobs, out)
