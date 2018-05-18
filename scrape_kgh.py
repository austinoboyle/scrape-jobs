from selenium.webdriver import Chrome
import json
from pprint import pprint
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def kgh():
    scraped_jobs = []

    KGH_CAREERS_URL = 'https://career5.successfactors.eu/career?company=KGH&career_ns=job_listing_summary&navBarLevel=JOB_SEARCH&_s.crb=lcJWb0ftX8PpE5Ez4PvdEQmYLSw%3d'
    driver = Chrome()
    driver.get(KGH_CAREERS_URL)

    try:
        element = WebDriverWait(driver, 10).until(
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

    for job in jobs:
        job_dict = {}

        link = job.find_element_by_css_selector(
            'a.jobTitle').get_attribute('href')
        job_dict['URL'] = link

        name = job.find_element_by_css_selector('a.jobTitle')
        job_dict['Title'] = name.text
        job_dict['Company'] = 'Kingston General Hospital'

        descriptions = job.find_elements_by_css_selector('span.jobContentEM')
        descriptions_col = ['ID', 'Open_Date', 'Category']
        for title, col in zip(descriptions_col, descriptions):
            job_dict[title] = col.text

        job_dict['Sectors'] = []

        for sector in sectors:
            for syn in data[sector]:
                if(syn in job_dict['Title']):
                    job_dict['Sectors'].append(sector)
                    break

        scraped_jobs.append(job_dict)


    with open('./json_files/kgh_jobs.json', 'w') as out:
        json.dump(scraped_jobs, out)
