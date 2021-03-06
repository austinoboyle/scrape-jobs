# Author: Cesur Kavaslar, 5/16/2018

# In command line, run:
# 	pip install beautifulsoup4
#	pip install requests

import requests
from bs4 import BeautifulSoup
import json


def keys():
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
            job_dict = {}

            # Get Job Title
            title = j.find(class_="col-sm-4").find('a').text.split('(#')[0].strip()
            job_dict['title'] = title
            # Get company
            company = j.find(class_="col-sm-4").find('small').text.strip()
            job_dict['company'] = company

            # Get URL, use to get description and industry
            job_url = str("http://keys.ca" + j.find('a').get('href'))
            job_dict['url'] = job_url
            job_page = requests.get(job_url)
            job_soup = BeautifulSoup(job_page.text, 'html.parser')

            try:
                img_src = job_soup.find(class_="printme").find(
                    'p').find('img')['src']
                img = "http://www.keys.ca" + img_src
            except:
                img = 'http://www.keys.ca/assets/image/logo/logo_basic.png'

            # Catch if not an accepted file format
            if (not img.endswith('png')) and (not img.endswith('jpeg')):
                # Set to default img
                img = 'http://www.keys.ca/assets/image/logo/logo_basic.png'
            job_dict['img'] = img

            industry = job_soup.find(class_="printme").find(
                'small').text[16:].strip()
            job_dict['category'] = industry
            description = job_soup.find(class_="printme").findAll('p')[2].text
            job_dict['description'] = description

            # Append job to positions array
            postions.append(job_dict)

    # Dump positions to json
    with open('../json_files/keys_jobs.json', 'w') as out:
        json.dump(postions, out)
