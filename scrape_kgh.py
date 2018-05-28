from selenium import webdriver
import json
from pprint import pprint
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def kgh():
    scraped_jobs = []
    # Get URL, use to get info
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")

    KGH_CAREERS_URL = 'https://career5.successfactors.eu/career?company=KGH&career_ns=job_listing_summary&navBarLevel=JOB_SEARCH&_s.crb=lcJWb0ftX8PpE5Ez4PvdEQmYLSw%3d'
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(KGH_CAREERS_URL)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.jobTitle"))
        )
    except:
        print("TIMEOUT EXCEPTION")
        driver.quit()

    with open('sectors.json') as data_file:
        data = json.load(data_file)
    sectors = []
    for header in data:
        sectors.append(header)

    jobs = driver.find_elements_by_css_selector('tr.jobResultItem')

    # Add to job dictionary
    for job in jobs:
        job_dict = {}

        link = job.find_element_by_css_selector(
            'a.jobTitle').get_attribute('href')
        job_dict['url'] = link

        name = job.find_element_by_css_selector('a.jobTitle')
        job_dict['title'] = name.text
        job_dict['company'] = 'Kingston General Hospital'
        job_dict['img'] = 'https://s3.ca-central-1.amazonaws.com/beadonorca/uploads/KGH_vertstack_tag_col_FB-259dcedf563525b7c0152df0f5dfb0cc.jpg'

        descriptions = job.find_elements_by_css_selector('span.jobContentEM')
        descriptions_col = ['id', 'openDate', 'category']
        for title, col in zip(descriptions_col, descriptions):
            job_dict[title] = col.text

        job_dict['sectors'] = []

        # Determine sectors of job
        for sector in sectors:
            for syn in data[sector]:
                if(syn.lower() in job_dict['title'].lower()):
                    job_dict['sectors'].append(sector)
                    break

        # Append job to positions array
        scraped_jobs.append(job_dict)

    # Dump positions to json
    with open('./json_files/kgh_jobs.json', 'w') as out:
        json.dump(scraped_jobs, out)
