from selenium.webdriver import Chrome
import json
from pprint import pprint

INDEED_CAREERS_URL = 'https://ca.indeed.com/jobs?q=&l=Kingston%2C+ON'
driver = Chrome()
driver.get(INDEED_CAREERS_URL)

scraped_jobs = []
jobs = driver.find_elements_by_css_selector('div.row.result.clickcard')
for job in jobs:
    job_dict = {}
    name = job.find_element_by_css_selector('a.jobtitle, a.turnstileLink')
    job_dict['Title'] = name.text
    company = job.find_element_by_css_selector('span.company')
    job_dict['Company'] = company.text
    link = job.find_element_by_css_selector(
        'a.jobtitle, a.turnstileLink').get_attribute('href')
    job_dict['URL'] = link
    scraped_jobs.append(job_dict)

with open('indeed_jobs.json', 'w') as out:
    json.dump(scraped_jobs, out)
