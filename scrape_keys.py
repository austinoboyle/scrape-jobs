# Author: Cesur Kavaslar, 5/16/2018

# In command line, run:
# 	pip install beautifulsoup4
#	pip install requests

import requests
from bs4 import BeautifulSoup
import json
content_titles = ['Title', 'Company', 'URL', 'Category', 'Description']


postions = []

# Iterate through every page
for page_num in range(1, 22):
    # Build the new url for the page
    url = 'http://keys.ca/jobboard/search.php?page=' + str(page_num)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    list_of_jobs = soup.find_all(class_="row job")  # class="col-sm-4"

    # Go through each resulting jobs
    for j in list_of_jobs:

        # Company and Title Stored Together
        # .replace("'", "\\\'")
        title_and_company = str(j.find(class_="col-sm-4").text)
        t_and_c_arr = title_and_company.split('(#')

        # Split Company and Title
        title = t_and_c_arr[0].strip()
        company = t_and_c_arr[1][5:].strip()

        # Get URL, use to get description and industry
        job_url = str("http://keys.ca" + j.find('a').get('href'))
        job_page = requests.get(job_url)
        job_soup = BeautifulSoup(job_page.text, 'html.parser')

        industry = job_soup.find(class_="printme").find(
            'small').text[16:].strip()
        description = job_soup.find(class_="printme").findAll('p')[2].text

        # Join all content into an array
        content = [title, company, job_url, industry, description]
        job = {}

        # Add to job dictionary
        for i in range(len(content_titles)):
            job[content_titles[i]] = content[i]

        # Append job to positions array
        postions.append(job)

# Dump positions to json
with open('keys_jobs.json', 'w') as out:
    json.dump(postions, out)
