# Import
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from pprint import pprint
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Import all scraping scripts
from scrape_city import city
from scrape_keys import keys
from scrape_glassdoor import glassdoor
from scrape_indeed import indeed
from scrape_kgh import kgh
from scrape_queens import queens
from scrape_slc import slc

# Run all scripts
def run():
    print("Run all started at "+ str(datetime.now()))
    # Scrape websites
    scrape()
    # Run combine script
    combine()
    # Filter out duplicates
    filter_dups()
    # Add sectors
    sectors()
    # Add skills to each job
    get_skills()
    # Print the time it ended
    print("Run all ended at "+ str(datetime.now()))

# Scrape all jobs
def scrape():
    try:
        print("City started at "+ str(datetime.now()))
        city()
    except:
        print("City failed")
    try:
        # print("Glassdoor started at "+ str(datetime.now()))
        # glassdoor()
        raise Exception('Glassdoor being skipped')
    except:
        print("Glassdoor failed")
    try:
        print("Indeed started at "+ str(datetime.now()))
        indeed()
    except:
        print("Indeed failed")
    try:
        print("Keys started at "+ str(datetime.now()))
        keys()
    except:
        print("Keys failed")
    try:
        print("Kgh started at "+ str(datetime.now()))
        kgh()
    except:
        print("Kgh failed")
    try:
        print("Queens started at "+ str(datetime.now()))
        queens()
    except:
        print("Queens failed")
    try:
        print("Slc started at "+ str(datetime.now()))
        slc()
    except:
        print("Slc failed")

# Combine all jobs to jobs.json
def combine():
    print("File combining started at "+ str(datetime.now()))
    full_arr = []

    # Try to read each of the individual job files

    try: # Try to read glassdoor jobs
        glassdoor_file = open('../json_files/glassdoor_jobs.json')
        glassdoor_arr  = json.load(glassdoor_file)
        full_arr = full_arr +  glassdoor_arr
    except:
        print("Glassdoor file read failed.")

    try: # Try to read indeed jobs
        indeed_file = open('../json_files/indeed_jobs.json')
        indeed_arr = json.load(indeed_file)
        full_arr = full_arr +  indeed_arr
    except:
        print("Indeed file read failed.")

    try: # Try to read keys jobs
        keys_file = open('../json_files/keys_jobs.json')
        keys_arr = json.load(keys_file)
        full_arr = full_arr +  keys_arr
    except:
        print("Keys file read failed.")

    try: # Try to read queens jobs
        queens_file = open('../json_files/queens_jobs.json')
        queens_arr = json.load(queens_file)
        full_arr = full_arr + queens_arr
    except:
        print("Queens file read failed.")

    try: # Try to read slc jobs
        slc_file = open('../json_files/slc_jobs.json')
        slc_arr  = json.load(slc_file)
        full_arr = full_arr +  slc_arr
    except:
        print("Slc file read failed.")

    try: # Try to read city jobs
        city_file = open('../json_files/city_jobs.json')
        city_arr = json.load(city_file)
        full_arr = full_arr + city_arr
    except:
        print("City file read failed.")

    try: # Try to read kgh jobs
        kgh_file = open('../json_files/kgh_jobs.json')
        kgh_arr = json.load(kgh_file)
        full_arr = full_arr +  kgh_arr
    except:
        print("Kgh file read failed.")


    # Dump resulting combined job array to json file
    with open('../json_files/jobs.json', 'w') as out:
        json.dump(full_arr, out)


# Filter out duplicate jobs
def filter_dups():
    print("Filtering duplicates started at "+ str(datetime.now()))
    # Access jobs file
    jobs_file = open('../json_files/jobs.json')
    # Read into array
    jobs_arr = json.load(jobs_file)
    # Empty array for filtered jobs
    filtered_arr = []

    # Iterate through every job
    for job in jobs_arr:
        dup = False
        # Check against each element in filtered jobs array
        for filtered_job in filtered_arr:
            # Check if title and company are duplicates
            title_dup = job['title'] == filtered_job['title']
            company_dup = job['company'] == filtered_job['company']
            # Set flag and pass if it is a duplicate
            if title_dup and company_dup:
                dup = True
                pass
        # If not in filtered jobs, append it
        if dup == False:
            filtered_arr.append(job)

    # Dump to json file
    with open('../json_files/jobs.json', 'w') as out:
        json.dump(filtered_arr, out)

def sectors():
    print("Get sectors started at "+ str(datetime.now()))
    # Access jobs file
    jobs_file = open('../json_files/jobs.json')
    # Read into array
    jobs_arr = json.load(jobs_file)

    # Access sectors file
    with open('../sectors/sectors.json') as data_file:
        data = json.load(data_file)
    sectors = []
    for header in data:
        sectors.append(header)

    # Iterate through jobs
    for job in jobs_arr:
        # Determine sectors
        job['sectors'] = []
        for sector in sectors:
            for syn in data[sector]:
                if(syn.lower() in job['title'].lower()):
                    job['sectors'].append(sector)
                    break

    # Dump to json file
    with open('../json_files/jobs.json', 'w') as out:
        json.dump(jobs_arr, out)

# Get the required skills for each job
def get_skills():
    print("Get skills started at "+ str(datetime.now()))

    # Access jobs file
    jobs_file = open('../json_files/jobs.json', encoding="utf8")
    jobs_arr = json.load(jobs_file)

    # Access skills file
    # skills_file = open('../skills/short_skills.json')
    skills_file = open('C:/Users/cesurk/Desktop/git_projects/pdf-parser/skills_linkedin_clean.json')
    skills_arr = json.load(skills_file)["skills"]

    # Iterate through every job
    for job in jobs_arr:
        # Instantiate an empty required skills array
        req_skills = []
        for skill in skills_arr:
            try:
                concat = (job['title'] + " " + job['description'])
                # If skill in description, add to required skills
                if skill in (job['title'] + " " + job['description']):
                    req_skills.append(skill)
            except:
                pass
        # Add to skills section of job
        job['skills'] = req_skills

    # Dump to json file
    with open('../json_files/jobs_with_skills.json', 'w') as out:
        json.dump(jobs_arr, out)


# Start
run()
