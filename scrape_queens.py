from selenium.webdriver import Chrome
import json
from pprint import pprint

QUEENS_CAREERS_URL = 'https://queensu.njoyn.com/cl4/xweb/Xweb.asp?tbtoken=Zl5aRR8XCB1xEHQDN1AmCCM%2FBmdEcCJfBkgjWiwME2UtXEQSXUdpcWMuJS5ALiRedQkbUxFaS3cqWA%3D%3D&chk=dFlbQBJe&page=joblisting&CLID=74827'
driver = Chrome()
driver.get(QUEENS_CAREERS_URL)


scraped_jobs = []
NUM_COLS = 6
col_titles = ['Number', 'Title', 'Category', 'Type', 'Open Date', 'Close Date']

table = driver.find_element_by_id('searchtable')
jobs = table.find_elements_by_tag_name('tr')

for job in jobs:
    job_dict = {}
    cols = job.find_elements_by_tag_name('td')
    for i, col in enumerate(cols):
        job_dict[col_titles[i]] = col.text
    scraped_jobs.append(job_dict)

print(job_dict)
with open('jobs.json', 'w') as out:
    json.dump(scraped_jobs, out)
