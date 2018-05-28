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
from combined_jobs import combine
from _filter_duplicates import filter

# Run all scripts
def run_all():
    print("Run all started at "+ str(datetime.now()))
    city()
    glassdoor()
    indeed()
    keys()
    kgh()
    queens()
    slc()
    # Run combine script
    combine()
    # Filter out duplicates
    filter()
    print("Run all ended at "+ str(datetime.now()))

run_all()
