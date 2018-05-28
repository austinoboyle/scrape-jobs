from selenium import webdriver
import json
from pprint import pprint

def glassdoor():
    scraped_jobs = []
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    # options.add_argument("--disable-gpu")
    # options.add_argument("--log-level=3")

    # Get sectors file
    with open('sectors.json') as data_file:
        data = json.load(data_file)
    sectors = []
    for header in data:
        sectors.append(header)

    # Instantiate web drivers; one to get list of jobs, one for description
    driver = webdriver.Chrome(chrome_options=options)
    desc_driver = webdriver.Chrome(chrome_options=options)

    # Iterate through every page
    for page_num in range(1, 19):
        # Get URL, use to get info
        GLASSDOOR_CAREERS_URL = 'https://www.glassdoor.ca/Job/kingston-jobs-SRCH_IL.0,8_IC2288886_IP' + str(page_num) + '.htm'
        driver.get(GLASSDOOR_CAREERS_URL)

        # Scroll the entire height of the page
        scheight = .1
        while scheight < 9.9:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scheight)
            scheight += .01

        # Get list of all jobs on this page
        table = driver.find_element_by_css_selector('ul.jlGrid.hover')
        jobs = table.find_elements_by_css_selector('li.jl')

        # Add the job info to the job dictionary
        for job in jobs:
            # Instantiate job dictionary
            job_dict = {}

            # Get title
            title = job.find_element_by_class_name('flexbox').text.strip()
            job_dict['title'] = title

            # Get company
            company = job.find_element_by_css_selector('div.flexbox.empLoc').find_element_by_css_selector('div').text.strip()
            job_dict['company'] = company

            # Get link
            link = job.find_element_by_class_name('jobLink').get_attribute('href')
            job_dict['url'] = link

            # Try to get lazy loaded logo
            try:
                job_dict['img'] = job.find_element_by_css_selector('span.sqLogo.tighten.smSqLogo').find_element_by_css_selector('img.lazy.lazy-loaded').get_attribute('data-original-2x')
            except: # If unable, use default glassdoor logo
                job_dict['img'] = 'https://media.glassdoor.com/brand-logo/green-stacked-logo/glassdoor-logo.jpg'

            # Go to the job's link
            desc_driver.get(link)

            # Click the "Read More" button for full description
            try:
                desc_driver.find_element_by_css_selector('div.readMore').click()
            except:
                pass # Button not found
            # Try to get description
            try:
                job_dict['description'] = desc_driver.find_element_by_css_selector('div.jobDescriptionContent.desc.module.pad').text
            except:
                job_dict['description'] = ""

            # Get type of employement from description and title
            desc = job_dict['title'].lower() + job_dict['description'].lower()
            if ("full-time" in desc) or ("full time" in desc):
                job_dict['type'] = "Full Time"
            elif ("part-time" in desc) or ("part time" in desc):
                job_dict['type'] = "Part Time"
            else:
                job_dict['type'] = ""

            # Determine sectors of job
            job_dict['sectors'] = []
            for sector in sectors:
                for syn in data[sector]:
                    if(syn.lower() in job_dict['title'].lower()):
                        job_dict['sectors'].append(sector)
                        break
            # Append job to positions array
            scraped_jobs.append(job_dict)

    # Close web drivers
    driver.close()
    desc_driver.close()


    # Dump positions to json
    with open('./json_files/glassdoor_jobs.json', 'w') as out:
        json.dump(scraped_jobs, out)

glassdoor()
