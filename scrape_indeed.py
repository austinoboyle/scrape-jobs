from selenium import webdriver
import json
from pprint import pprint


def indeed():
    scraped_jobs = []

    with open('sectors.json') as data_file:
        data = json.load(data_file)
    sectors = []
    for header in data:
        sectors.append(header)

    for page_num in range(0, 9):
        INDEED_CAREERS_URL = 'https://ca.indeed.com/jobs?q=&l=Kingston%2C+ON&start=' + \
            str(page_num)+"0"
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(INDEED_CAREERS_URL)

        jobs = driver.find_elements_by_css_selector('div.row.result.clickcard')
        for job in jobs:
            job_dict = {}
            name = job.find_element_by_css_selector(
                'a.jobtitle, a.turnstileLink')
            job_dict['Title'] = name.text
            company = job.find_element_by_css_selector('span.company')
            job_dict['Company'] = company.text
            link = job.find_element_by_css_selector(
                'a.jobtitle, a.turnstileLink').get_attribute('href')
            job_dict['URL'] = link

            job_dict['Sectors'] = []

            for sector in sectors:
                for syn in data[sector]:
                    if(syn in job_dict['Title']):
                        job_dict['Sectors'].append(sector)
                        break

            scraped_jobs.append(job_dict)

    with open('./json_files/indeed_jobs.json', 'w') as out:
        json.dump(scraped_jobs, out)
