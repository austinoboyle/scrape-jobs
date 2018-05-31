from selenium import webdriver
import json
import requests
from bs4 import BeautifulSoup


def indeed():
    scraped_jobs = []
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(chrome_options=options)
    job_driver = webdriver.Chrome(chrome_options=options)

    # Iterate through every page
    for page_num in range(0, 9):
        # Get URL, use to get info
        INDEED_CAREERS_URL = 'https://ca.indeed.com/jobs?q=&l=Kingston%2C+ON&start=' + \
            str(page_num)+"0"

        driver.get(INDEED_CAREERS_URL)

        jobs = driver.find_elements_by_css_selector('div.row.result.clickcard')

        # Add to job dictionary
        num_jobs = len(jobs)
        for i in range(num_jobs):
            jobs = driver.find_elements_by_css_selector(
                'div.row.result.clickcard')
            job = jobs[i]
            job_dict = {}
            name = job.find_element_by_css_selector(
                'a.jobtitle, a.turnstileLink')
            job_dict['title'] = name.text
            company = job.find_element_by_css_selector('span.company')
            job_dict['company'] = company.text
            link = job.find_element_by_css_selector(
                'a.jobtitle, a.turnstileLink').get_attribute('href')
            job_dict['url'] = link

            job_driver.get(link)
            # Get image from link
            try:
                img = job_driver.find_element_by_css_selector(
                    'img.cmp_logo_img').get_attribute('src')
                job_dict['img'] = img
            except:
                job_dict['img'] = "https://d3v8fhblas9eb9.cloudfront.net/i/wp-content/uploads/2014/07/indeed-logo1.png"\
            # Get description from link
            try:
                desc = job_driver.find_element_by_css_selector('td.snip')
                job_dict['description'] = desc.text
            except:
                job_dict['description'] = ""

            # Append job to positions array
            scraped_jobs.append(job_dict)

    # Close driver
    driver.close()

    # Dump positions to json
    with open('../json_files/indeed_jobs.json', 'w') as out:
        json.dump(scraped_jobs, out)
