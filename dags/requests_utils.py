from datetime import datetime
from bs4 import BeautifulSoup
from pandas import json_normalize

import requests
import pandas as pd
import json

def request_url(url):
    return requests.get(url)

def _extracting_data():
    where='köln' #where='d%C3%BCsseldorf'
    category='data+engineer' #category='data+scientist'
    URL = f'https://de.indeed.com/jobs?q={category}&l={where}'
    page = request_url(URL)

    if(page.status_code == 200):
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(id='resultsCol')
        today = datetime.today()
        
        job_elems = results.find_all('div', class_='jobsearch-SerpJobCard')
        job_list = []

        for job_elem in job_elems:
            title_elem = job_elem.find('h2', class_='title')
            company_elem = job_elem.find('span', class_='company')
            location_elem = job_elem.find('span', class_='location')
            link_elm = job_elem.find('a')
            
            if None in (title_elem, company_elem, location_elem):
                continue
            else:
                job = {
                    'date': today,
                    'title':title_elem.text.strip().replace('\n','').replace('neu',''),
                    'company':company_elem.text.strip(),
                    'location':location_elem.text.strip(),
                    'link': f'https://de.indeed.com{link_elm["href"]}',
                }
            
                job_list.append(job)
    
        processed_jobs = json_normalize(job_list)
        processed_jobs.to_csv('data/processed_jobs.csv', index=None, header=False)