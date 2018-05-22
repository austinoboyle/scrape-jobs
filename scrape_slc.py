# Author: Cesur Kavaslar, 5/16/2018

# In command line, run:
# 	pip install beautifulsoup4
#	pip install requests

import requests
from bs4 import BeautifulSoup
import json


def slc():
    content_titles = ['title', 'company', 'type', 'url', 'education', 'closeDate'] #, 'category', 'description']
    postions = []

    # Get sectors
    with open('sectors.json') as data_file:
        data = json.load(data_file)
    sectors = []
    for header in data:
        sectors.append(header)

    # Get the url
    url = 'http://slc.totalhire.com/postings.php?l%5B-1%5D%5B%5D=l_10'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    #list_of_jobs = soup.find_all(id="data", {"class" : lambda L: L and L.startswith('row')})
    table = soup.find('table')
    list_of_jobs = table.find_all(class_="row1") + table.find_all(class_="row2")
    #print(list_of_jobs)
    # Go through each resulting jobs
    for j in list_of_jobs:

        title = j.find(class_="dbgrab_Position_Title").text
        company = j.find(class_="dbgrab_Company_Name").text
        type = j.find(class_="dbgrab_Type").text
        job_url = "http://slc.totalhire.com/posting-view.php?p=" + j.find(class_="dbgrab_").find('a').get('name')

        # Get more infor from the job url
        job_page = requests.get(job_url)
        job_soup = BeautifulSoup(job_page.text, 'html.parser')
        job_cats = job_soup.find_all(class_="row")
        education = ""
        closeDate = ""
        for cat in job_cats:
            key = cat.find(class_="title").text.strip()
            value = cat.find(class_="response").text.strip()
            if ("Minimum Education Required" in key):
                education = value
            if ("Closing Date" in key):
                closeDate = value


        content = [title, company, type, job_url, education, closeDate]
        job_dict = {}

        # Add to job dictionary
        for i in range(len(content_titles)):
            job_dict[content_titles[i]] = content[i]

        # Determine sectors of job
        job_dict['sectors'] = []
        for sector in sectors:
            for syn in data[sector]:
                if(syn.lower() in job_dict['title'].lower()):
                    job_dict['sectors'].append(sector)
                    break

        # Append job to positions array
        postions.append(job_dict)

    # Dump positions to json
    with open('./json_files/slc_jobs.json', 'w') as out:
        json.dump(postions, out)
