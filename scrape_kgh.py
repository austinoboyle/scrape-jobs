from selenium import webdriver
import json
from pprint import pprint
import os

scraped_jobs = []

KGH_CAREERS_URL = 'https://career5.successfactors.eu/career?company=KGH&career_ns=job_listing_summary&navBarLevel=JOB_SEARCH&_s.crb=lcJWb0ftX8PpE5Ez4PvdEQmYLSw%3d'
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(chrome_options=options)
driver.get(KGH_CAREERS_URL)

jobs = driver.find_elements_by_css_selector('tr.jobResultItem')

for job in jobs:
    job_dict = {}
    name = job.find_element_by_css_selector('a.jobTitle')
    job_dict['Title'] = name.text
    #category = job.find_element_by_css_selector('span.jobContentEM')
    #job_dict['Category'] = category.text
    # link = job.find_element_by_css_selector(
    #    'a.jobtitle, a.turnstileLink').get_attribute('href')
    #job_dict['URL'] = link
    scraped_jobs.append(job_dict)

outDir = str(os.getenv('OUTDIR'))
with open(outDir+'kgh_jobs.json', 'w') as out:
    json.dump(scraped_jobs, out)
